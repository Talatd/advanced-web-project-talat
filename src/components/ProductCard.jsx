import React from 'react';
import { ShoppingCart } from 'lucide-react';
import { motion } from 'framer-motion';

const ProductCard = ({ product, addToCart }) => {
    return (
        <motion.div
            className="glass"
            whileHover={{ y: -10, boxShadow: '0 10px 30px -10px rgba(102, 252, 241, 0.4)' }}
            style={{ overflow: 'hidden', display: 'flex', flexDirection: 'column' }}
        >
            <div style={{ height: '220px', overflow: 'hidden' }}>
                <img
                    src={product.image}
                    alt={product.name}
                    style={{ width: '100%', height: '100%', objectFit: 'cover', transition: 'transform 0.5s' }}
                    onMouseOver={e => e.currentTarget.style.transform = 'scale(1.1)'}
                    onMouseOut={e => e.currentTarget.style.transform = 'scale(1)'}
                />
            </div>
            <div className="flex-col gap-4" style={{ padding: '1.5rem', flex: 1, justifyContent: 'space-between' }}>
                <div>
                    <span className="text-accent text-sm font-bold uppercase tracking-wider">{product.category}</span>
                    <h3 className="text-xl mt-4" style={{ color: '#fff', marginBottom: '0.5rem' }}>{product.name}</h3>
                    <p className="text-secondary text-sm">{product.description}</p>
                </div>

                <div className="flex items-center justify-between mt-8">
                    <span className="text-2xl font-bold" style={{ color: '#fff' }}>${product.price}</span>
                    <button className="btn btn-primary" onClick={() => addToCart(product)}>
                        <ShoppingCart size={18} /> Add
                    </button>
                </div>
            </div>
        </motion.div>
    );
};

export default ProductCard;
