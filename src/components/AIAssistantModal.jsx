import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Bot, Sparkles, Send, Loader2, ShoppingCart, Users, CheckCircle2, AlertCircle, Cpu } from 'lucide-react';

const API_BASE = import.meta.env.VITE_API_URL || (import.meta.env.PROD ? '' : 'http://localhost:8000');

const AIAssistantModal = ({ isOpen, onClose, addToCart, products }) => {
    const [messages, setMessages] = useState([
        {
            role: 'assistant',
            content: "👋 Hello! I'm the **SmartBuy CrewAI Agent** — your multi-agent shopping advisor.\n\nI use **3 specialized AI agents** working together:\n\n🔍 **Product Recommender** — finds ideal products\n💰 **Budget Analyst** — evaluates cost & value\n🔗 **Compatibility Checker** — ensures everything works together\n\nTell me what you need! For example:\n- *\"I need a gaming setup\"*\n- *\"Best budget peripherals\"*\n- *\"A monitor for design work\"*"
        }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [backendStatus, setBackendStatus] = useState('checking');
    const [recommendedIds, setRecommendedIds] = useState([]);
    const chatEndRef = useRef(null);

    useEffect(() => {
        if (isOpen) {
            checkBackendHealth();
        }
    }, [isOpen]);

    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const checkBackendHealth = async () => {
        try {
            const res = await fetch(`${API_BASE}/api/health`);
            if (res.ok) {
                const data = await res.json();
                setBackendStatus(data.mode || 'online');
            } else {
                setBackendStatus('offline');
            }
        } catch {
            setBackendStatus('offline');
        }
    };

    const handleSend = async () => {
        if (!input.trim() || isLoading) return;

        const userMessage = input.trim();
        setInput('');
        setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
        setIsLoading(true);

        // Add "thinking" message
        setMessages(prev => [...prev, {
            role: 'system',
            content: '🧠 CrewAI agents are collaborating...\n\n`Agent 1` → Analyzing your needs...\n`Agent 2` → Evaluating budget options...\n`Agent 3` → Checking compatibility...'
        }]);

        try {
            const res = await fetch(`${API_BASE}/api/recommend`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: userMessage })
            });

            if (!res.ok) throw new Error('API request failed');

            const data = await res.json();

            // Remove the "thinking" message and add the real response
            setMessages(prev => {
                const filtered = prev.filter(m => m.role !== 'system');
                return [...filtered, {
                    role: 'assistant',
                    content: data.result,
                    productIds: data.recommended_product_ids,
                    agentInfo: data.agent_info
                }];
            });

            setRecommendedIds(data.recommended_product_ids || []);
        } catch (error) {
            setMessages(prev => {
                const filtered = prev.filter(m => m.role !== 'system');
                return [...filtered, {
                    role: 'assistant',
                    content: '⚠️ Could not reach the CrewAI backend. Make sure the Python server is running:\n\n```\ncd backend\npip install -r requirements.txt\npython main.py\n```\n\nThe server should be available at `http://localhost:8000`',
                    isError: true
                }];
            });
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    const handleAddRecommended = () => {
        if (products && recommendedIds.length > 0) {
            recommendedIds.forEach(id => {
                const product = products.find(p => p.id === id);
                if (product && addToCart) {
                    addToCart(product);
                }
            });
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: `✅ Added ${recommendedIds.length} recommended item(s) to your cart! Head to the cart page to review.`
            }]);
            setRecommendedIds([]);
        }
    };

    const renderMarkdown = (text) => {
        if (!text) return '';

        let html = text
            // Headers
            .replace(/^### (.+)$/gm, '<h4 class="ai-h4">$1</h4>')
            .replace(/^## (.+)$/gm, '<h3 class="ai-h3">$1</h3>')
            // Bold
            .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
            // Italic
            .replace(/\*(.+?)\*/g, '<em>$1</em>')
            // Inline code
            .replace(/`(.+?)`/g, '<code class="ai-code">$1</code>')
            // Code blocks
            .replace(/```([\s\S]*?)```/g, '<pre class="ai-pre">$1</pre>')
            // Horizontal rule
            .replace(/^---$/gm, '<hr class="ai-hr" />')
            // Line breaks  
            .replace(/\n/g, '<br/>');

        return html;
    };

    return (
        <AnimatePresence>
            {isOpen && (
                <>
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="ai-modal-overlay"
                        onClick={onClose}
                    />
                    <motion.div
                        initial={{ opacity: 0, y: 50, scale: 0.9 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: 20, scale: 0.95 }}
                        className="ai-modal-container glass"
                    >
                        {/* Header */}
                        <div className="ai-modal-header">
                            <div className="flex items-center gap-3">
                                <div className="ai-bot-icon">
                                    <Bot size={24} />
                                </div>
                                <div>
                                    <h2 style={{ margin: 0, fontSize: '1.1rem' }}>SmartBuy CrewAI</h2>
                                    <div className="ai-status-row">
                                        <Users size={12} />
                                        <span>3 Agents</span>
                                        <span className={`ai-status-dot ${backendStatus === 'offline' ? 'offline' : 'online'}`} />
                                        <span style={{ fontSize: '0.65rem' }}>
                                            {backendStatus === 'checking' ? 'Connecting...' :
                                                backendStatus === 'offline' ? 'Offline' :
                                                    backendStatus === 'demo' ? 'Demo Mode' : 'Live'}
                                        </span>
                                    </div>
                                </div>
                            </div>
                            <button className="btn-icon" onClick={onClose}><X size={22} /></button>
                        </div>

                        {/* Agent Info Banner */}
                        <div className="ai-agent-banner">
                            <div className="ai-agent-chip">
                                <Cpu size={13} />
                                <span>Product Recommender</span>
                            </div>
                            <div className="ai-agent-chip">
                                <Cpu size={13} />
                                <span>Budget Analyst</span>
                            </div>
                            <div className="ai-agent-chip">
                                <Cpu size={13} />
                                <span>Compatibility Checker</span>
                            </div>
                        </div>

                        {/* Chat Messages */}
                        <div className="ai-chat-messages">
                            {messages.map((msg, idx) => (
                                <motion.div
                                    key={idx}
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    className={`ai-message ${msg.role}`}
                                >
                                    {msg.role === 'assistant' && (
                                        <div className="ai-message-avatar">
                                            {msg.isError ? <AlertCircle size={16} /> : <Sparkles size={16} />}
                                        </div>
                                    )}
                                    {msg.role === 'system' && (
                                        <div className="ai-message-avatar system">
                                            <Loader2 size={16} className="ai-spinner" />
                                        </div>
                                    )}
                                    <div
                                        className={`ai-message-bubble ${msg.role} ${msg.isError ? 'error' : ''}`}
                                    >
                                        <div dangerouslySetInnerHTML={{ __html: renderMarkdown(msg.content) }} />
                                        
                                        {/* Display Agents Used (LangGraph Visibility) */}
                                        {msg.agentInfo?.agents_used && (
                                            <div className="ai-agents-list">
                                                {msg.agentInfo.agents_used.map((agent, i) => (
                                                    <span key={i} className="ai-agent-tag">
                                                        {agent.includes('LangGraph') ? <Sparkles size={10} /> : <Cpu size={10} />}
                                                        {agent}
                                                    </span>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                </motion.div>
                            ))}

                            {/* Add to Cart Button */}
                            {recommendedIds.length > 0 && !isLoading && (
                                <motion.div
                                    initial={{ opacity: 0, scale: 0.9 }}
                                    animate={{ opacity: 1, scale: 1 }}
                                    className="ai-add-cart-row"
                                >
                                    <button className="btn btn-primary ai-add-cart-btn" onClick={handleAddRecommended}>
                                        <ShoppingCart size={18} />
                                        Add {recommendedIds.length} Recommended Item{recommendedIds.length > 1 ? 's' : ''} to Cart
                                    </button>
                                </motion.div>
                            )}

                            <div ref={chatEndRef} />
                        </div>

                        {/* Input Area */}
                        <div className="ai-input-area">
                            <input
                                type="text"
                                className="ai-input"
                                placeholder="Ask about products, setups, or recommendations..."
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyDown={handleKeyDown}
                                disabled={isLoading}
                            />
                            <button
                                className="btn btn-primary ai-send-btn"
                                onClick={handleSend}
                                disabled={isLoading || !input.trim()}
                            >
                                {isLoading ? <Loader2 size={18} className="ai-spinner" /> : <Send size={18} />}
                            </button>
                        </div>
                    </motion.div>
                </>
            )}
        </AnimatePresence>
    );
};

export default AIAssistantModal;
