import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import axios from 'axios'
import './ProductDetail.css'

const API_URL = 'http://127.0.0.1:8000'

function ProductDetail() {
    const { id } = useParams()
    const [product, setProduct] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fetchProduct()
    }, [id])

    const fetchProduct = async () => {
        try {
            const response = await axios.get(`${API_URL}/products/${id}`)
            setProduct(response.data)
        } catch (error) {
            console.error('Error fetching product:', error)
        } finally {
            setLoading(false)
        }
    }

    if (loading) return <div className="loading">Loading...</div>
    if (!product) return <div className="error">Product not found</div>

    const productUrl = product.product_url || `https://hunnit.com/search?q=${encodeURIComponent(product.title)}`

    return (
        <div className="product-detail">
            <Link to="/" className="back-button">← Back to Products</Link>

            <div className="detail-container">
                <div className="image-section">
                    <img
                        src={product.image_url || "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='400'%3E%3Crect fill='%238B1538' width='400' height='400'/%3E%3Ctext fill='white' font-size='24' font-family='Arial' x='50%25' y='50%25' text-anchor='middle' dy='.3em'%3EHunnit Activewear%3C/text%3E%3C/svg%3E"}
                        alt={product.title}
                    />
                </div>

                <div className="info-section">
                    <h1>{product.title}</h1>
                    <p className="price">₹{product.price}</p>
                    <p className="category">{product.category}</p>

                    <div className="description">
                        <h3>Description</h3>
                        <p>{product.description}</p>
                    </div>

                    {product.features && Object.keys(product.features).length > 0 && (
                        <div className="features">
                            <h3>Features</h3>
                            <ul>
                                {Object.entries(product.features).map(([key, value]) => (
                                    <li key={key}><strong>{key}:</strong> {value}</li>
                                ))}
                            </ul>
                        </div>
                    )}

                    <a
                        href={productUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="view-button"
                    >
                        View on Website →
                    </a>
                </div>
            </div>
        </div>
    )
}

export default ProductDetail
