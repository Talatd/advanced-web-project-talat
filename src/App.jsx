import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Catalog from './pages/Catalog';
import Cart from './pages/Cart';
import AIAssistantModal from './components/AIAssistantModal';
import { products } from './data/products';

function App() {
  const [cartItems, setCartItems] = useState([]);
  const [isAiModalOpen, setIsAiModalOpen] = useState(false);

  const addToCart = (product) => {
    setCartItems([...cartItems, product]);
  };

  const removeFromCart = (index) => {
    const newCart = [...cartItems];
    newCart.splice(index, 1);
    setCartItems(newCart);
  };

  const clearCart = () => {
    if (cartItems.length > 0) {
      alert("Demo Order placed successfully! (AI Agent integration for processing in next assignment)");
      setCartItems([]);
    }
  };

  return (
    <Router>
      <div className="app-container">
        <Navbar cartCount={cartItems.length} onOpenAiModal={() => setIsAiModalOpen(true)} />

        <main>
          <Routes>
            <Route path="/" element={<Home addToCart={addToCart} onOpenAiModal={() => setIsAiModalOpen(true)} />} />
            <Route path="/catalog" element={<Catalog addToCart={addToCart} />} />
            <Route path="/cart" element={<Cart cartItems={cartItems} removeFromCart={removeFromCart} clearCart={clearCart} />} />
          </Routes>
        </main>

        <AIAssistantModal
          isOpen={isAiModalOpen}
          onClose={() => setIsAiModalOpen(false)}
          addToCart={addToCart}
          products={products}
        />

        <footer className="glass" style={{ margin: '4rem 0 0 0', padding: '2rem', textAlign: 'center', borderTop: '1px solid var(--glass-border)' }}>
          <p className="text-secondary text-sm">
            © 2026 SmartBasket. Advanced Web Homework 2 — CrewAI Integration.
          </p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
