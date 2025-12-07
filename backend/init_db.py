from backend.database import engine, Base
from backend.models import Product
from sqlalchemy import text

def init_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

if __name__ == "__main__":
    init_db()
