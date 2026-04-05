import React from 'react';
import { ShoppingCart, Bot, Zap, Package } from 'lucide-react';
import { Link } from 'react-router-dom';

const Navbar = ({ cartCount, onOpenAiModal }) => {
    return (
        <header className="glass-header py-4">
            <div className="container flex items-center justify-between">
                <Link to="/" className="flex items-center gap-2">
                    <Zap className="text-accent" size={32} />
                    <h1 className="text-2xl" style={{ margin: 0 }}>SmartBasket</h1>
                </Link>
                <nav>
                    <ul className="flex items-center gap-6 font-bold" style={{ margin: 0 }}>
                        <li>
                            <Link to="/catalog" className="flex items-center gap-2" style={{ transition: 'color 0.3s' }} onMouseOver={e => e.currentTarget.style.color = 'var(--accent-color)'} onMouseOut={e => e.currentTarget.style.color = ''}>
                                <Package size={20} /> Catalog
                            </Link>
                        </li>
                        <li>
                            <Link to="/cart" className="flex items-center gap-2 position-relative" style={{ position: 'relative', transition: 'color 0.3s' }} onMouseOver={e => e.currentTarget.style.color = 'var(--accent-color)'} onMouseOut={e => e.currentTarget.style.color = ''}>
                                <ShoppingCart size={20} /> Cart
                                {cartCount > 0 && <span className="badge">{cartCount}</span>}
                            </Link>
                        </li>
                        <li>
                            <button onClick={onOpenAiModal} className="btn btn-outline" style={{ padding: '0.4rem 1rem' }}>
                                <Bot size={20} /> Ask AI
                            </button>
                        </li>
                    </ul>
                </nav>
            </div>
        </header>
    );
};

export default Navbar;
