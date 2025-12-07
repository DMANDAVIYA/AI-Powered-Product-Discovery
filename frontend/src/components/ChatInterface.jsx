import { useState, useRef, useEffect } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'
import './ChatInterface.css'

const API_URL = 'https://neusearch-backend-x9lv.onrender.com'

function ChatInterface() {
    const [messages, setMessages] = useState([
        { role: 'assistant', content: 'Hi! I can help you find the perfect activewear. What are you looking for?' }
    ])
    const [input, setInput] = useState('')
    const [loading, setLoading] = useState(false)
    const messagesEndRef = useRef(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }

    useEffect(() => {
        scrollToBottom()
    }, [messages])

    const handleSubmit = async (e) => {
        e.preventDefault()
        if (!input.trim() || loading) return

        const userMessage = input.trim()
        setInput('')
        setMessages(prev => [...prev, { role: 'user', content: userMessage }])
        setLoading(true)

        try {
            const response = await axios.post(`${API_URL}/chat`, { query: userMessage })

            setMessages(prev => [...prev, {
                role: 'assistant',
                content: response.data.response,
                products: response.data.products
            }])
        } catch (error) {
            console.error('Error:', error)
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: 'Sorry, I encountered an error. Please try again.'
            }])
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="chat-interface">
            <div className="chat-header">
                <h3>AI Shopping Assistant</h3>
            </div>

            <div className="chat-messages">
                {messages.map((msg, idx) => (
                    <div key={idx} className={`message ${msg.role}`}>
                        <div className="message-content">{msg.content}</div>

                        {msg.products && msg.products.length > 0 && (
                            <div className="product-recommendations">
                                {msg.products.map((product) => (
                                    <Link to={`/product/${product.id}`} key={product.id} className="rec-product-card">
                                        {product.image_url && (
                                            <img src={product.image_url} alt={product.title} />
                                        )}
                                        <div>
                                            <h4>{product.title}</h4>
                                            <p className="price">${product.price}</p>
                                        </div>
                                    </Link>
                                ))}
                            </div>
                        )}
                    </div>
                ))}
                {loading && (
                    <div className="message assistant">
                        <div className="message-content typing">Thinking...</div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            <form onSubmit={handleSubmit} className="chat-input-form">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask me anything about our products..."
                    disabled={loading}
                />
                <button type="submit" disabled={loading || !input.trim()}>
                    Send
                </button>
            </form>
        </div>
    )
}

export default ChatInterface
