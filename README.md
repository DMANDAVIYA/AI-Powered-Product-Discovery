# AI-Powered Product Discovery Assistant

An intelligent e-commerce assistant that helps users discover products through natural language conversations. Built with advanced RAG (Retrieval-Augmented Generation) techniques, combining semantic search, keyword matching, and GPT-4 to provide personalized product recommendations.

## Live Demo

**Frontend:** https://ai-powered-discovery-product-6.vercel.app/  
**Backend API:** https://neusearch-backend-x9lv.onrender.com  
**API Documentation:** https://neusearch-backend-x9lv.onrender.com/docs

---

## Features

### User Experience
- **Conversational AI Shopping** - Ask questions in natural language like "I need comfortable black leggings under $50"
- **Smart Product Discovery** - AI understands intent and recommends relevant products
- **Interactive Chat Interface** - Persistent conversation with clickable product recommendations
- **Product Gallery** - Browse all products with images, prices, and details
- **Responsive Design** - Works seamlessly on desktop and mobile

### Technical Capabilities
- **Hybrid Search** - Combines semantic understanding (vector search) with keyword matching
- **Intelligent Filtering** - Automatically extracts price ranges, colors, and categories from queries
- **AI Re-ranking** - GPT-4 re-ranks results to ensure top recommendations are most relevant
- **Automated Web Scraping** - Dynamically discovers and extracts product data from Hunnit.com
- **Vector Embeddings** - Uses OpenAI embeddings for semantic product search

---

## Architecture

### System Overview

The application follows a modern full-stack architecture with clear separation of concerns:

```
User Interface (React)
        ↓
    REST API (FastAPI)
        ↓
    RAG Pipeline
    ↙         ↘
PostgreSQL   ChromaDB
(Products)   (Vectors)
           ↓
    OpenAI GPT-4
```

### Components

**Frontend (React + Vite)**
- Product grid with search and filters
- Individual product detail pages
- AI chat interface with streaming responses
- Deployed on Vercel

**Backend (FastAPI + Python)**
- RESTful API with automatic documentation
- RAG pipeline for intelligent product recommendations
- Web scraping with Firecrawl API
- Deployed on Render with Docker

**Databases**
- **PostgreSQL** - Stores product data (title, price, description, images)
- **ChromaDB** - Stores vector embeddings for semantic search

**AI Services**
- **OpenAI GPT-4** - Conversational AI and response generation
- **OpenAI Embeddings** - Text-to-vector conversion for semantic search
- **Firecrawl API** - Web scraping and content extraction

---

## How It Works

### 1. Data Collection (Web Scraping)

The system automatically scrapes product data from Hunnit.com using a multi-step process:

1. **Discovery** - Firecrawl's map function discovers all product URLs automatically
2. **Extraction** - Each product page is scraped for title, price, description, and images
3. **Storage** - Structured data is saved to PostgreSQL
4. **Embedding** - Vector embeddings are generated and stored in ChromaDB

**Result:** 25+ products with complete metadata ready for intelligent search

### 2. Product Search (RAG Pipeline)

When a user asks a question, the system processes it through four stages:

**Stage 1: Query Understanding**
- GPT-4 analyzes the user's natural language question
- Extracts structured filters (price range, category, color, keywords)
- Example: "black leggings under $50" becomes structured filters

**Stage 2: Hybrid Retrieval**
- **Semantic Search** - ChromaDB finds products similar in meaning
- **Keyword Search** - PostgreSQL finds exact keyword matches
- **Fusion** - Combines both result sets with weighted scoring

**Stage 3: Re-ranking**
- GPT-4 re-evaluates top 10 results for relevance to original query
- Ensures best matches appear first

**Stage 4: Response Generation**
- GPT-4 generates a natural, conversational response
- Includes top 5 product recommendations with reasoning
- Returns structured data for frontend to display

**Result:** Accurate, relevant product recommendations with natural language explanations

---

## Technology Stack

### Backend
- **FastAPI** - Modern Python web framework with automatic OpenAPI documentation
- **PostgreSQL** - Relational database for structured product data
- **ChromaDB** - Vector database for semantic search embeddings
- **SQLAlchemy** - Python ORM for database operations
- **Pydantic** - Data validation and settings management
- **OpenAI API** - GPT-4 for chat and text-embedding-3-small for vectors
- **Firecrawl API** - Web scraping and content extraction

### Frontend
- **React 18** - UI library with modern hooks
- **Vite** - Next-generation frontend build tool
- **React Router** - Client-side routing
- **Axios** - HTTP client for API communication
- **CSS3** - Modern styling with gradients and animations

### Infrastructure
- **Docker** - Containerization for consistent deployment
- **Render** - Backend hosting (PostgreSQL database + FastAPI service)
- **Vercel** - Frontend hosting with automatic deployments

---

## Project Structure

```
AI-Powered-Product-Discovery/
├── backend/
│   ├── main.py              # FastAPI app, routes, CORS configuration
│   ├── rag.py               # RAG pipeline implementation
│   ├── scraper.py           # Firecrawl web scraping logic
│   ├── vector_store.py      # ChromaDB operations
│   ├── database.py          # PostgreSQL connection and session management
│   ├── models.py            # SQLAlchemy database models
│   ├── import_db.py         # Import products from JSON backup
│   ├── export_db.py         # Export products to JSON backup
│   ├── init_db.py           # Create database tables
│   └── requirements.txt     # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Home.jsx           # Product grid page
│   │   │   ├── Home.css
│   │   │   ├── ProductDetail.jsx  # Single product view
│   │   │   └── ProductDetail.css
│   │   ├── components/
│   │   │   ├── ChatInterface.jsx  # AI chat component
│   │   │   └── ChatInterface.css
│   │   ├── App.jsx                # Router setup
│   │   └── main.jsx               # React entry point
│   ├── package.json
│   └── vite.config.js
│
├── chroma_db/               # ChromaDB vector storage (local)
├── products_backup.json     # Product data backup for deployment
├── Dockerfile              # Docker container configuration
├── .env.example            # Environment variables template
├── DEPLOYMENT.md           # Detailed deployment guide
└── README.md               # This file
```

---

## Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 17
- OpenAI API key
- Firecrawl API key

### Local Development Setup

1. **Clone the repository**

2. **Set up environment variables**
   - Copy `.env.example` to `.env`
   - Add your API keys and database URL

3. **Backend Setup**
   - Create and activate virtual environment
   - Install dependencies from `requirements.txt`
   - Initialize database with `python -m backend.init_db`
   - Either scrape fresh data or import from backup
   - Start server with `uvicorn backend.main:app --reload --port 8000`

4. **Frontend Setup**
   - Navigate to `frontend/` directory
   - Install dependencies with `npm install`
   - Start dev server with `npm run dev`

Visit http://localhost:5173 to see the application running locally.

---

## API Endpoints

### Products
- `GET /` - Health check
- `GET /products` - List all products (supports pagination)
- `GET /products/{id}` - Get single product details

### AI Chat
- `POST /chat` - Send message to AI assistant
  - Request body: `{"query": "user question"}`
  - Response: `{"response": "AI answer", "products": [...]}`

### Admin
- `POST /scrape` - Trigger web scraping
- `POST /init-db` - Create database tables
- `POST /import-backup` - Import products from JSON backup

Full interactive API documentation available at `/docs` endpoint.

---

## Design Decisions

### Why Hybrid Search?
Combining semantic and keyword search provides comprehensive coverage:
- **Semantic search** understands intent and meaning ("comfortable" → soft fabrics)
- **Keyword search** catches exact matches ("leggings")
- **Together** they ensure no relevant products are missed

### Why Separate Databases?
- **PostgreSQL** - Optimized for structured, relational data with ACID compliance
- **ChromaDB** - Specialized for fast vector similarity search
- **Separation** allows independent scaling and optimization for each use case

### Why RAG Over Fine-tuning?
- No training data required
- Easy to update with new products
- More transparent and debuggable
- Cost-effective for small to medium catalogs
- Maintains up-to-date product information

### Why Firecrawl Over BeautifulSoup?
- Handles JavaScript-rendered content automatically
- Automatic URL discovery with map function
- Built-in rate limiting and error handling
- Cleaner, more reliable data extraction
- Better handling of dynamic websites

---

## Challenges and Solutions

### Challenge 1: pgvector Installation on Windows
**Problem:** PostgreSQL on Windows doesn't include the pgvector extension by default  
**Solution:** Store embeddings as JSON in PostgreSQL, use ChromaDB for vector search operations

### Challenge 2: Firecrawl Rate Limits
**Problem:** Free tier has 2 concurrent browsers limit  
**Solution:** Implemented sequential scraping with 2-second delays, created backup/restore system for deployment

### Challenge 3: Cold Starts on Render Free Tier
**Problem:** Service sleeps after 15 minutes of inactivity  
**Solution:** First request takes ~30 seconds to wake up, acceptable for demo purposes

### Challenge 4: CORS Between Vercel and Render
**Problem:** Frontend on Vercel needs to communicate with backend on Render  
**Solution:** Implemented regex-based CORS to allow all `*.vercel.app` domains

### Challenge 5: Database Migration Between Environments
**Problem:** ChromaDB vector database difficult to migrate  
**Solution:** Created JSON backup system, re-create embeddings on import in new environment

---

## Performance Metrics

- **Scraping:** Approximately 25 products in 60 seconds
- **Chat Response:** 2-3 seconds (including AI processing)
- **Product Load:** Under 500ms (with caching)
- **Vector Search:** Under 100ms (ChromaDB)
- **Database Queries:** Under 50ms (PostgreSQL)

---

## Future Improvements

- Add user authentication and personalized recommendations
- Implement product filters (price slider, category dropdown)
- Add shopping cart functionality
- Implement multi-turn conversation memory
- Add product comparison feature
- Implement A/B testing for RAG pipeline optimization
- Add analytics dashboard for insights
- Optimize for mobile with Progressive Web App
- Add product reviews and ratings
- Implement collaborative filtering recommendation engine

---

## Security

### Current Implementation

**API Security**
- CORS configured to allow only specific domains (localhost and Vercel)
- Environment variables for sensitive data (API keys, database URLs)
- No API keys exposed in frontend code
- HTTPS enforced on production deployments

**Database Security**
- PostgreSQL with password authentication
- Connection strings stored in environment variables
- No SQL injection vulnerabilities (using SQLAlchemy ORM)
- Database hosted on Render's secure infrastructure

**API Rate Limiting**
- Firecrawl API has built-in rate limiting
- OpenAI API has usage limits per account
- No public endpoints that could be abused


---

## Database Migration

### Migration Strategy

The application uses a backup/restore approach for database migration to avoid Firecrawl API costs during deployment:

**Export Process (Local)**
1. Run `python -m backend.export_db` to create `products_backup.json`
2. Exports all product data including metadata
3. Commit backup file to repository

**Import Process (Production)**
1. Deploy backend with `products_backup.json` included
2. Run `POST /init-db` to create database tables
3. Run `POST /import-backup` to populate database
4. System automatically generates embeddings for ChromaDB

### Why This Approach?

**Advantages:**
- Saves Firecrawl API credits (no re-scraping needed)
- Faster deployment (no waiting for scraping)
- Consistent data across environments
- Easy rollback to previous data state

**Trade-offs:**
- Manual step required after deployment
- Embeddings regenerated (uses OpenAI credits)
- No automatic data sync between environments

### Alternative: Fresh Scraping

For fresh data, use the `/scrape` endpoint:
1. Deploy backend without importing backup
2. Run `POST /scrape` to scrape live data
3. Wait ~60 seconds for completion
4. Products automatically stored in both databases

### Database Schema

**Products Table (PostgreSQL)**
- `id` - Primary key
- `title` - Product name
- `price` - Product price
- `description` - Product description
- `image_url` - Product image URL
- `category` - Product category
- `product_url` - Link to original product page
- `features` - JSON field for additional metadata
- `created_at` - Timestamp

**Vector Store (ChromaDB)**
- Document: Concatenated title + description
- Embedding: 1536-dimension vector (OpenAI)
- Metadata: Product ID, price, category

---

## Deployment

The application is deployed using modern cloud platforms:

**Backend (Render)**
- PostgreSQL database hosted on Render
- FastAPI service containerized with Docker
- Automatic deployments from GitHub
- Environment variables managed in Render dashboard

**Frontend (Vercel)**
- React application built with Vite
- Automatic deployments from GitHub
- Root directory set to `frontend/`
- Environment variables for API endpoints


