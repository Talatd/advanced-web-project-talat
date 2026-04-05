import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { Bot, ChevronRight, Zap } from 'lucide-react';
import { products } from '../data/products';
import ProductCard from '../components/ProductCard';

const Home = ({ addToCart, onOpenAiModal }) => {
    const featured = products.slice(0, 3);

    return (
        <div className="animate-fade-in">
            <section className="hero-gradient" style={{ minHeight: '80vh', display: 'flex', alignItems: 'center' }}>
                <div className="container flex-col gap-8 text-center" style={{ padding: '6rem 20px', alignItems: 'center' }}>
                    <motion.div
                        initial={{ scale: 0.8, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        transition={{ duration: 0.8 }}
                        className="flex items-center justify-center gap-4 mb-6"
                    >
                        <div className="glass" style={{ padding: '1rem', borderRadius: '50%', color: 'var(--accent-color)' }}>
                            <Zap size={48} />
                        </div>
                    </motion.div>
                    <motion.h1
                        initial={{ y: 20, opacity: 0 }}
                        animate={{ y: 0, opacity: 1 }}
                        transition={{ delay: 0.2 }}
                        className="text-4xl"
                        style={{ fontSize: '4rem', fontWeight: 900, lineHeight: 1.1 }}
                    >
                        Welcome to the <br /> Future of <span className="text-accent">E-Commerce</span>
                    </motion.h1>
                    <motion.p
                        initial={{ y: 20, opacity: 0 }}
                        animate={{ y: 0, opacity: 1 }}
                        transition={{ delay: 0.4 }}
                        className="text-xl text-secondary text-center"
                        style={{ maxWidth: '600px', margin: '0 auto 2rem' }}
                    >
                        Discover state-of-the-art gadgets specifically curated. Our forthcoming AI Shopping Assistant will completely revolutionize how you find your perfect tech setup.
                    </motion.p>
                    <motion.div
                        initial={{ y: 20, opacity: 0 }}
                        animate={{ y: 0, opacity: 1 }}
                        transition={{ delay: 0.6 }}
                        className="flex justify-center gap-4"
                    >
                        <Link to="/catalog" className="btn btn-primary" style={{ padding: '1rem 2.5rem', fontSize: '1.25rem' }}>
                            Shop Now <ChevronRight />
                        </Link>
                        <button className="btn btn-outline" style={{ padding: '1rem 2.5rem', fontSize: '1.25rem' }} onClick={onOpenAiModal}>
                            <Bot /> Talk to AI
                        </button>
                    </motion.div>
                </div>
            </section>

            <section className="container py-16">
                <div className="flex justify-between items-center mb-8">
                    <h2 className="text-4xl">Featured Tech</h2>
                    <Link to="/catalog" className="btn btn-outline">View All</Link>
                </div>

                <div className="grid grid-cols-3 md-grid-cols-2 sm-grid-cols-1 gap-6">
                    {featured.map((p) => (
                        <ProductCard key={p.id} product={p} addToCart={addToCart} />
                    ))}
                </div>
            </section>
        </div>
    );
};

export default Home;
