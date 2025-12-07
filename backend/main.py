from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, validator

from .database import get_db, engine, Base
from .models import Product
from .scraper import scrape_hunnit
from .rag import chat_with_products

# Initialize DB (can also be done via init_db.py)
# Base.metadata.create_all(bind=engine)

app = FastAPI(title="Neusearch AI API")

# CORS - Update allowed origins for production
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    # Vercel deployment (will be updated after deployment)
    "https://*.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.vercel\.app",  # Allow all Vercel domains
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class ProductResponse(BaseModel):
    id: int
    title: str
    price: float
    description: str
    image_url: Optional[str] = None
    category: Optional[str] = None
    product_url: Optional[str] = None
    features: Optional[dict] = None
    
    class Config:
        orm_mode = True

class ChatRequest(BaseModel):
    query: str
    
    @validator('query')
    def validate_query(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("Query cannot be empty")
        if len(v) > 500:
            raise ValueError("Query too long. Maximum 500 characters")
        return v.strip()

class ChatResponse(BaseModel):
    response: str
    products: List[ProductResponse]

@app.get("/")
def read_root():
    return {"message": "Neusearch AI Backend is running"}

@app.post("/scrape")
def trigger_scrape():
    try:
        scrape_hunnit()
        return {"message": "Scraping completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/import-backup")
def import_backup():
    """Import products from JSON backup file"""
    try:
        from .import_db import import_database
        import_database()
        return {"message": "Database import completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products", response_model=List[ProductResponse])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        result = chat_with_products(request.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
