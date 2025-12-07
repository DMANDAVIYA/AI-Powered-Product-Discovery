import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'
import ChatInterface from '../components/ChatInterface'
import './Home.css'

const API_URL = 'http://127.0.0.1:8000'

function Home() {
    const [products, setProducts] = useState([])
    const [loading, setLoading] = useState(true)
    const [showChat, setShowChat] = useState(false)

    useEffect(() => {
        fetchProducts()
    }, [])

    const fetchProducts = async () => {
        try {
            const response = await axios.get(`${API_URL}/products`)
            setProducts(response.data)
        } catch (error) {
            console.error('Error fetching products:', error)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="home">
            <header className="header">
                <h1>AI-Powered Product Discovery</h1>
            </header>

            <div className="container">
                {loading ? (
                    <div className="loading">Loading products...</div>
                ) : (
                    <div className="product-grid">
                        {products.map((product) => (
                            <Link to={`/product/${product.id}`} key={product.id} className="product-card">
                                {product.image_url && (
                                    <img src={product.image_url} alt={product.title} />
                                )}
                                <div className="product-info">
                                    <h3>{product.title}</h3>
                                    <p className="price">₹{product.price}</p>
                                    <p className="category">{product.category}</p>
                                </div>
                            </Link>
                        ))}
                    </div>
                )}
            </div>

            <button
                className="chat-toggle"
                onClick={() => setShowChat(!showChat)}
            >
                {showChat ? (
                    <span>✕ Close</span>
                ) : (
                    <span>
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                        </svg>
                        <span style={{ marginLeft: '8px' }}>CHAT</span>
                    </span>
                )}
            </button>

            {showChat && <ChatInterface />}
        </div>
    )
}

export default Home
