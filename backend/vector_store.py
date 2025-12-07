import chromadb
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize Chroma Client
# We'll use a persistent client stored in the 'chroma_db' folder
client = chromadb.PersistentClient(path="chroma_db")

# Use OpenAI Embedding Function
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=OPENAI_API_KEY,
    model_name="text-embedding-3-small"
)

# Get or Create Collection
collection = client.get_or_create_collection(
    name="products",
    embedding_function=openai_ef
)

def add_products_to_vector_db(products: List[Dict]):
    """
    Add products to ChromaDB.
    products list should contain dicts with: id, title, description, price, category
    """
    if not products:
        return

    ids = [str(p["id"]) for p in products]
    documents = [f"{p['title']}. {p['description']}" for p in products]
    metadatas = [
        {
            "title": p["title"],
            "price": p["price"],
            "category": p["category"],
            "product_id": p["id"]
        } 
        for p in products
    ]

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )
    print(f"Indexed {len(products)} products in ChromaDB.")

def query_vector_db(query_text: str, n_results: int = 20, where: Dict = None):
    """
    Query ChromaDB for relevant products.
    """
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        where=where
    )
    return results
