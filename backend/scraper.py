import os
import json
import time
from firecrawl import FirecrawlApp
from sqlalchemy.orm import Session
from .models import Product
from .database import SessionLocal
from dotenv import load_dotenv
import re

load_dotenv()

FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

def scrape_hunnit():
    """
    Scrape Hunnit.com using Firecrawl's batch_scrape method.
    """
    app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)
    
    collection_url = "https://hunnit.com/collections/all"
    
    print(f"Step 1: Mapping {collection_url} to find product URLs...")
    
    # Use map to get all product URLs
    try:
        map_result = app.map(collection_url)
        # map_result is a MapData object with 'links' attribute
        links = map_result.links if hasattr(map_result, 'links') else []
        
        # Extract URLs from link objects
        all_urls = []
        for link in links:
            if hasattr(link, 'url'):
                all_urls.append(link.url)
            elif isinstance(link, str):
                all_urls.append(link)
        
        # Filter for product URLs
        product_urls = [url for url in all_urls if '/products/' in url][:30]
        print(f"Found {len(product_urls)} product URLs")
        
        if len(product_urls) < 25:
            print(f"Warning: Only found {len(product_urls)} products, need at least 25")
            if len(product_urls) == 0:
                return
            
    except Exception as e:
        print(f"Map failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print(f"\nStep 2: Scraping {min(len(product_urls), 25)} products individually...")
    
    # Scrape products individually (Firecrawl free plan works better this way)
    scraped_data = []
    for i, url in enumerate(product_urls[:25], 1):
        try:
            print(f"  {i}/25: {url.split('/')[-1][:40]}...")
            result = app.scrape(url)
            if result:
                scraped_data.append(result)
            time.sleep(2)  # Be nice to API
        except Exception as e:
            print(f"    Error: {e}")
            continue
    
    batch_result = {'data': scraped_data}
    
    print(f"\nStep 3: Processing {len(batch_result.get('data', []))} scraped products...")
    
    db = SessionLocal()
    count = 0
    
    for item in batch_result['data']:
        if count >= 25:
            break
            
        try:
            # Extract data
            metadata_dict = item.metadata.__dict__ if hasattr(item, 'metadata') and hasattr(item.metadata, '__dict__') else {}
            markdown = item.markdown if hasattr(item, 'markdown') else ''
            url = metadata_dict.get('source_url', metadata_dict.get('url', ''))
            
            if not url:
                continue
                
            # Extract title
            title = metadata_dict.get('title') or metadata_dict.get('og_title')
            if not title or title == 'None':
                # Extract from URL
                url_parts = url.split('/')[-1].split('-')
                title = ' '.join(word.capitalize() for word in url_parts)
            elif '|' in title:
                title = title.split('|')[0].strip()
                
            description = metadata_dict.get('description') or metadata_dict.get('og_description', markdown[:500])
            image_url = metadata_dict.get('og_image', '')
            
            # Price extraction
            price = 0.0
            price_match = re.search(r'(?:Rs\.|₹|\$)\s?(\d+(?:,\d+)*(?:\.\d{2})?)', markdown)
            if price_match:
                try:
                    price = float(price_match.group(1).replace(',', ''))
                except:
                    pass
                    
            # Check if exists
            existing = db.query(Product).filter(Product.product_url == url).first()
            if existing:
                continue
                
            # Create product
            new_product = Product(
                title=title,
                price=price,
                description=description,
                features={},
                image_url=image_url,
                category="Activewear",
                product_url=url
            )
            
            db.add(new_product)
            count += 1
            print(f"  {count}. {title} (${price})")
            
        except Exception as e:
            print(f"  Error processing product: {e}")
            continue
    
    db.commit()
    
    # Index to ChromaDB
    from .vector_store import add_products_to_vector_db
    
    products_to_index = []
    products = db.query(Product).all()
    for p in products:
        products_to_index.append({
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "price": p.price,
            "category": p.category
        })
        
    add_products_to_vector_db(products_to_index)
    
    db.close()
    print(f"\n✓ Successfully scraped {count} products and indexed in Vector DB.")

if __name__ == "__main__":
    scrape_hunnit()
