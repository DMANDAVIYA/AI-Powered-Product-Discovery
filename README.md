# Neusearch AI - Product Discovery Assistant

An AI-powered product discovery assistant that recommends products based on natural language queries using advanced RAG (Retrieval-Augmented Generation) pipeline.

## 🎯 Features

- **Smart Product Scraping**: Automatically scrapes product data from Hunnit.com using Firecrawl API
- **Advanced RAG Pipeline**: 
  - Hybrid Search (Semantic + Keyword)
  - Self-Querying (LLM extracts filters from natural language)
  - Re-ranking for maximum relevance
- **Vector Database**: ChromaDB for semantic search
- **Conversational AI**: Chat interface powered by OpenAI GPT-4
- **Clean UI**: React frontend with product grid, detail pages, and chat interface

## 🏗️ Architecture

### Backend (FastAPI + PostgreSQL)
- **FastAPI**: RESTful API with automatic documentation
- **PostgreSQL**: Relational database for product data
- **ChromaDB**: Vector database for embeddings
- **OpenAI**: Embeddings (text-embedding-3-small) + Chat (GPT-4)
- **Firecrawl**: Web scraping API

### Frontend (React + Vite)
- **React Router**: Client-side routing
- **Axios**: HTTP client
- **Modern CSS**: Gradient designs, animations

### RAG Pipeline
1. **Query Understanding**: LLM extracts structured filters (price, category) from user query
2. **Hybrid Retrieval**: 
   - Semantic search via ChromaDB (vector similarity)
   - Keyword search via PostgreSQL (full-text)
   - Fusion of results
3. **Re-ranking**: LLM re-ranks top results for relevance
4. **Generation**: GPT-4 generates conversational response with product recommendations

## 📦 Installation

### Prerequisites
- Python 3.12+
- Node.js 18+
- PostgreSQL 17
- API Keys: Firecrawl, OpenAI

### Setup

1. **Clone the repository**
```bash
git clone <your-repo>
cd neusearch
```

2. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys and database URL
```

3. **Backend Setup**
```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r backend/requirements.txt

# Initialize database
python -m backend.init_db

# Run scraper (scrapes 25+ products)
python -m backend.scraper

# Start backend server
uvicorn backend.main:app --reload --port 8000
```

4. **Frontend Setup**
```bash
cd frontend
npm install
npm run dev
```

## 🚀 Usage

1. **Browse Products**: Visit http://localhost:5173 to see all products
2. **View Details**: Click any product to see full details
3. **Chat with AI**: Click the chat button (💬) to ask questions like:
   - "Looking for something I can wear in the gym and also in meetings"
   - "I need comfortable leggings for yoga under $50"
   - "What do you have for running?"

## 📁 Project Structure

```
neusearch/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── database.py          # DB connection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── scraper.py           # Firecrawl scraper
│   ├── rag.py               # RAG pipeline
│   ├── vector_store.py      # ChromaDB integration
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   └── ProductDetail.jsx
│   │   ├── components/
│   │   │   └── ChatInterface.jsx
│   │   └── App.jsx
│   └── package.json
├── .env.example
└── README.md
```

## 🔧 API Endpoints

- `GET /` - Health check
- `GET /products` - List all products
- `GET /products/{id}` - Get product details
- `POST /chat` - Chat with AI assistant
- `POST /scrape` - Trigger scraping

## 🎨 Design Decisions

### Scraping Approach
- Used Firecrawl's `map()` to automatically discover product URLs (no hardcoded URLs)
- Individual scraping with 2-second delays to respect rate limits
- Robust error handling and fallbacks

### RAG Pipeline
- **Hybrid Search** ensures both semantic understanding and exact keyword matches
- **Self-Querying** allows natural language filters ("under $50", "for gym")
- **Re-ranking** with LLM ensures top results are truly relevant

### Database Choice
- PostgreSQL for structured data (products)
- ChromaDB for vector embeddings (semantic search)
- Separation allows independent scaling

## 🚧 Challenges & Trade-offs

1. **pgvector Installation**: Windows PostgreSQL doesn't include pgvector by default, so we store embeddings as JSON
2. **Firecrawl Rate Limits**: Free plan has 2 concurrent browsers, so scraping is sequential
3. **Cost Optimization**: Using ChromaDB (local) instead of Pinecone to avoid cloud costs during development

## 🔮 Future Improvements

- Add pgvector for faster vector search
- Implement user authentication
- Add product filters (price range, category)
- Deploy to production (Render/Railway)
- Add Docker configuration
- Implement caching for faster responses
- Add analytics and user feedback

## 📝 License

MIT

## 👤 Author

Built for Neusearch AI Technical Assignment
