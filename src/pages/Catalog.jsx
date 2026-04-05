import React, { useState } from 'react';
import { products } from '../data/products';
import ProductCard from '../components/ProductCard';
import { Filter, Search } from 'lucide-react';
import { motion } from 'framer-motion';

const Catalog = ({ addToCart }) => {
    const [searchTerm, setSearchTerm] = useState('');
    const [category, setCategory] = useState('All');

    const categories = ['All', ...new Set(products.map(p => p.category))];

    const filteredProducts = products.filter(p => {
        const matchSearch = p.name.toLowerCase().includes(searchTerm.toLowerCase());
        const matchCat = category === 'All' ? true : p.category === category;
        return matchSearch && matchCat;
    });

    return (
        <div className="container py-16 animate-fade-in">
            <div className="text-center mb-12">
                <h2 className="text-4xl mb-4">Tech Catalog</h2>
                <p className="text-secondary text-lg">Browse our elite selection of futuristic gadgets.</p>
            </div>

            <div className="flex glass mb-8" style={{ padding: '1rem', flexWrap: 'wrap', gap: '1rem' }}>
                <div className="flex items-center gap-2 flex-grow" style={{ background: 'var(--bg-surface)', padding: '0.5rem 1rem', borderRadius: 'var(--border-radius)' }}>
                    <Search className="text-secondary" />
                    <input
                        type="text"
                        placeholder="Search products..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        style={{
                            background: 'transparent',
                            border: 'none',
                            color: 'white',
                            fontSize: '1rem',
                            width: '100%',
                            outline: 'none'
                        }}
                    />
                </div>

                <div className="flex items-center gap-2">
                    <Filter className="text-accent" />
                    <select
                        value={category}
                        onChange={(e) => setCategory(e.target.value)}
                        className="btn btn-outline"
                        style={{ padding: '0.5rem 1rem' }}
                    >
                        {categories.map(c => (
                            <option key={c} value={c} style={{ background: 'var(--bg-surface)', color: 'white' }}>{c}</option>
                        ))}
                    </select>
                </div>
            </div>

            {filteredProducts.length === 0 ? (
                <div className="text-center py-16 text-secondary text-xl">
                    No products found matching your criteria.
                </div>
            ) : (
                <motion.div
                    className="grid grid-cols-3 md-grid-cols-2 sm-grid-cols-1 gap-6"
                    initial="hidden"
                    animate="visible"
                    variants={{
                        hidden: { opacity: 0 },
                        visible: {
                            opacity: 1,
                            transition: { staggerChildren: 0.1 }
                        }
                    }}
                >
                    {filteredProducts.map(p => (
                        <ProductCard key={p.id} product={p} addToCart={addToCart} />
                    ))}
                </motion.div>
            )}
        </div>
    );
};

export default Catalog;
