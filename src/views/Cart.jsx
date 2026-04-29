import React from 'react';
import { Trash2, CreditCard } from 'lucide-react';
import { Link } from 'react-router-dom';

const Cart = ({ cartItems, removeFromCart, clearCart }) => {
    const total = cartItems.reduce((acc, item) => acc + item.price, 0);

    if (cartItems.length === 0) {
        return (
            <div className="container py-16 text-center animate-fade-in">
                <h2 className="text-4xl mb-6 text-secondary">Your Cart is Empty</h2>
                <Link to="/catalog" className="btn btn-primary">Start Shopping</Link>
            </div>
        );
    }

    return (
        <div className="container py-16 animate-fade-in">
            <h2 className="text-4xl mb-8">Shopping Cart</h2>

            <div className="grid md-grid-cols-3 gap-8" style={{ gridTemplateColumns: '2fr 1fr' }}>
                <div className="flex-col gap-4">
                    {cartItems.map((item, index) => (
                        <div key={`${item.id}-${index}`} className="glass flex items-center justify-between" style={{ padding: '1rem', borderRadius: 'var(--border-radius)' }}>
                            <div className="flex items-center gap-4">
                                <img src={item.image} alt={item.name} style={{ width: '80px', height: '80px', objectFit: 'cover', borderRadius: '8px' }} />
                                <div>
                                    <h4 className="text-xl" style={{ margin: 0 }}>{item.name}</h4>
                                    <span className="text-accent text-sm">{item.category}</span>
                                </div>
                            </div>
                            <div className="flex items-center gap-6 text-xl font-bold">
                                ${item.price.toLocaleString()}
                                <button className="btn-icon" style={{ color: 'var(--danger-color)' }} onClick={() => removeFromCart(index)}>
                                    <Trash2 size={20} />
                                </button>
                            </div>
                        </div>
                    ))}
                </div>

                <div className="glass" style={{ padding: '2rem', height: 'fit-content' }}>
                    <h3 className="text-2xl mb-6" style={{ borderBottom: '1px solid var(--glass-border)', paddingBottom: '1rem' }}>Order Summary</h3>
                    <div className="flex justify-between text-secondary mb-4">
                        <span>Subtotal</span>
                        <span>${total.toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between text-secondary mb-4">
                        <span>Shipping</span>
                        <span>$0.00</span>
                    </div>
                    <div className="flex justify-between text-xl font-bold mt-6" style={{ borderTop: '1px solid var(--glass-border)', paddingTop: '1rem' }}>
                        <span>Total</span>
                        <span className="text-accent">${total.toLocaleString()}</span>
                    </div>
                    <button className="btn btn-primary mt-8" style={{ width: '100%' }} onClick={clearCart}>
                        <CreditCard size={20} /> Checkout (Demo)
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Cart;
