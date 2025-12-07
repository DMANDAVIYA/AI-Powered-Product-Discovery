"""
Database Export Script
Exports PostgreSQL data and ChromaDB to files for migration
"""
import json
import os
from backend.database import SessionLocal
from backend.models import Product
import shutil

def export_database():
    """Export all products to JSON file"""
    db = SessionLocal()
    
    try:
        # Get all products
        products = db.query(Product).all()
        
        # Convert to dict
        products_data = []
        for p in products:
            products_data.append({
                'id': p.id,
                'title': p.title,
                'price': p.price,
                'description': p.description,
                'image_url': p.image_url,
                'category': p.category,
                'product_url': p.product_url,
                'features': p.features
            })
        
        # Save to JSON
        with open('products_backup.json', 'w', encoding='utf-8') as f:
            json.dump(products_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Exported {len(products_data)} products to products_backup.json")
        
        # Copy ChromaDB folder
        if os.path.exists('chroma_db'):
            if os.path.exists('chroma_db_backup'):
                shutil.rmtree('chroma_db_backup')
            shutil.copytree('chroma_db', 'chroma_db_backup')
            print(f"✅ Backed up ChromaDB to chroma_db_backup/")
        
        print("\n📦 Backup complete!")
        print("Files created:")
        print("  - products_backup.json (PostgreSQL data)")
        print("  - chroma_db_backup/ (Vector embeddings)")
        
    finally:
        db.close()

if __name__ == "__main__":
    export_database()
