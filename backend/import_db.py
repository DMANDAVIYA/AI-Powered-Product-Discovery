"""
Database Import Script
Imports products from JSON backup (no API calls needed!)
"""
import json
import os
from backend.database import SessionLocal
from backend.models import Product
from backend.vector_store import add_product_to_vector_db

def import_database():
    """Import products from JSON backup"""
    
    if not os.path.exists('products_backup.json'):
        print("❌ products_backup.json not found!")
        print("Run export_db.py first on your local machine")
        return
    
    db = SessionLocal()
    
    try:
        # Load JSON
        with open('products_backup.json', 'r', encoding='utf-8') as f:
            products_data = json.load(f)
        
        print(f"📥 Importing {len(products_data)} products...")
        
        # Clear existing products (optional)
        # db.query(Product).delete()
        
        # Import each product
        for data in products_data:
            # Create product
            product = Product(
                title=data['title'],
                price=data['price'],
                description=data['description'],
                image_url=data['image_url'],
                category=data['category'],
                product_url=data['product_url'],
                features=data['features']
            )
            
            db.add(product)
            db.commit()
            db.refresh(product)
            
            # Add to vector DB (uses existing embeddings if available)
            try:
                add_product_to_vector_db(product)
                print(f"✅ Imported: {product.title}")
            except Exception as e:
                print(f"⚠️  Vector error for {product.title}: {e}")
        
        print(f"\n✅ Successfully imported {len(products_data)} products!")
        print("✅ ChromaDB vectors created")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import_database()
