from sqlalchemy import Column, Integer, String, Float, Text, DateTime, JSON
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Float)
    description = Column(Text)
    features = Column(JSON)
    image_url = Column(String)
    category = Column(String, index=True)
    product_url = Column(String, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    
    # Vector embedding stored as JSON (pgvector not available)
    embedding = Column(JSON, nullable=True)



