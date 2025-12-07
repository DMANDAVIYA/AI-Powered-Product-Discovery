# Project Structure

```
neusearch/
├── backend/
│   ├── database.py          # Database connection & session management
│   ├── init_db.py           # Database initialization script
│   ├── main.py              # FastAPI application & API endpoints
│   ├── models.py            # SQLAlchemy database models
│   ├── rag.py               # RAG pipeline (search, retrieval, LLM)
│   ├── scraper.py           # Firecrawl web scraper
│   └── vector_store.py      # ChromaDB vector database integration
│
├── frontend/
│   ├── public/              # Static assets
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.jsx      # AI chat component
│   │   │   └── ChatInterface.css
│   │   ├── pages/
│   │   │   ├── Home.jsx               # Product listing page
│   │   │   ├── Home.css
│   │   │   ├── ProductDetail.jsx      # Product detail page
│   │   │   └── ProductDetail.css
│   │   ├── App.jsx          # Main app with routing
│   │   ├── App.css          # Global styles
│   │   ├── main.jsx         # React entry point
│   │   └── index.css        # Base CSS
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── chroma_db/               # Vector database storage (gitignored)
├── .env                     # Environment variables (gitignored)
├── .env.example             # Environment template
├── .gitignore
├── README.md                # Project documentation
├── SECURITY.md              # Security documentation
├── directions.md            # Original assignment
└── instructions.md          # Assignment requirements
```

## Core Files Count

**Backend:** 7 Python files
**Frontend:** 10 files (5 JSX + 5 CSS)
**Config:** 4 files (.env.example, .gitignore, README.md, SECURITY.md)

**Total:** Clean, minimal codebase with only essential files!
