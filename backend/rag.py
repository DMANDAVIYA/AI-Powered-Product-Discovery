import os
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_
from .models import Product
from .database import SessionLocal
import openai
from dotenv import load_dotenv
import json
import numpy as np
from .vector_store import query_vector_db

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def get_embedding(text: str) -> List[float]:
    """Generate embedding for text using OpenAI."""
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def extract_filters_and_query(user_query: str) -> Dict[str, Any]:
    """Use LLM to extract structured filters and a refined search query."""
    prompt = f"""
    Analyze the user query: "{user_query}"
    Extract a search query and any filters (category, min_price, max_price).
    Return JSON only.
    Example: {{"query": "gym wear", "filters": {{"category": "Activewear", "max_price": 50}}}}
    """
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a search assistant."},
                      {"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error extracting filters: {e}")
        return {"query": user_query, "filters": {}}

def hybrid_search(db: Session, query_text: str, filters: Dict, limit: int = 20):
    """Perform hybrid search: ChromaDB (Vector) + Keyword Match (DB)."""
    # 1. Vector Search via ChromaDB
    chroma_where = {}
    if filters.get("category"):
        chroma_where["category"] = filters["category"]
    
    try:
        vector_results = query_vector_db(
            query_text=query_text,
            n_results=limit,
            where=chroma_where if chroma_where else None
        )
        
        vector_ids = []
        if vector_results and vector_results.get('ids'):
            vector_ids = [int(id) for id in vector_results['ids'][0]]
        
        print(f"Vector search found {len(vector_ids)} IDs")
            
        if vector_ids:
            vector_products = db.query(Product).filter(Product.id.in_(vector_ids)).all()
        else:
            vector_products = []
        
        print(f"Vector products: {len(vector_products)}")
    except Exception as e:
        print(f"Vector search error: {e}")
        vector_products = []
    
    # 2. Keyword Search (DB)
    try:
        keyword_products = db.query(Product).filter(
            or_(
                Product.title.ilike(f"%{query_text}%"),
                Product.description.ilike(f"%{query_text}%")
            )
        ).limit(limit).all()
        
        print(f"Keyword search found {len(keyword_products)} products")
    except Exception as e:
        print(f"Keyword search error: {e}")
        keyword_products = []
    
    # 3. Fusion
    seen_ids = set()
    final_results = []
    
    for p in vector_products:
        if p.id not in seen_ids:
            final_results.append(p)
            seen_ids.add(p.id)
            
    for p in keyword_products:
        if p.id not in seen_ids:
            final_results.append(p)
            seen_ids.add(p.id)
    
    print(f"Combined results: {len(final_results)}")
            
    # Post-filter for price
    filtered = []
    for p in final_results:
        if filters.get("max_price") and p.price > filters["max_price"]:
            continue
        filtered.append(p)
    
    print(f"After filtering: {len(filtered)}")
        
    return filtered[:limit]

def chat_with_products(query: str):
    db = SessionLocal()
    
    # 1. Understand Query
    analysis = extract_filters_and_query(query)
    search_query = analysis.get("query", query)
    filters = analysis.get("filters", {})
    
    print(f"Searching for: {search_query} with filters: {filters}")
    
    # 2. Hybrid Search
    candidates = hybrid_search(db, search_query, filters, limit=20)
    
    # 3. Filter to exact title matches if available
    exact_matches = [p for p in candidates if query.lower() in p.title.lower()]
    
    if exact_matches:
        top_products = exact_matches[:5]
        print(f"Found {len(exact_matches)} exact title matches")
    else:
        top_products = candidates[:5]
        print(f"No exact matches, using top {len(top_products)} results")
    
    # 4. Generate Response
    if not top_products:
        return {
            "response": "I'm sorry, I couldn't find any products matching your query. Could you try searching for gym wear, leggings, sports bras, or other athletic clothing?",
            "products": []
        }
    
    # Build context with numbered list
    context_lines = []
    for i, p in enumerate(top_products, 1):
        desc = p.description[:100] if p.description else "Activewear product"
        context_lines.append(f"{i}. **{p.title}** - ₹{p.price}\n   {desc}")
    
    context = "\n\n".join(context_lines)
    
    system_prompt = f"""You are a helpful shopping assistant for Hunnit activewear.

I am showing you {len(top_products)} products that match the user's search for "{query}".

YOUR JOB: Recommend these products enthusiastically!

RULES:
- These products ARE available and match the search
- Mention product names and prices (₹)
- Be helpful and positive
- DO NOT say "we don't have" - we DO have these products!"""
    
    user_prompt = f"""User searched for: "{query}"

Here are the matching products:

{context}

Recommend these products to the user!"""
    
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3
    )
    
    return {
        "response": response.choices[0].message.content,
        "products": top_products
    }
