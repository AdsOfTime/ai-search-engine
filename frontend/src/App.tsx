import React from 'react';
import './App.css';
import { searchAPI } from './services/api';
import ProductCard from './components/ProductCard';
import { Product } from './types';

const App: React.FC = () => {
  const [searchQuery, setSearchQuery] = React.useState('');
  const [products, setProducts] = React.useState<Product[]>([]);
  const [loading, setLoading] = React.useState(false);
  const [hasSearched, setHasSearched] = React.useState(false);
  const [totalResults, setTotalResults] = React.useState(0);

  const categories = [
    {
      id: 'cosmetics',
      title: 'Cosmetics & Beauty',
      icon: '💄',
      description: 'Find the best makeup, skincare, and beauty products from top brands at competitive prices.'
    },
    {
      id: 'fashion', 
      title: 'Fashion & Style',
      icon: '👗',
      description: 'Discover trendy clothing, shoes, and accessories across multiple fashion retailers.'
    },
    {
      id: 'healthcare',
      title: 'Health & Wellness', 
      icon: '🏥',
      description: 'Compare prices on supplements, medications, and health products for your wellbeing.'
    }
  ];

  const handleCategoryClick = async (categoryId: string) => {
    setLoading(true);
    setHasSearched(true);
    try {
      const results = await searchAPI.searchProducts({ 
        q: '', 
        category: categoryId === 'cosmetics' ? 'makeup' : categoryId 
      });
      setProducts(results.products);
      setTotalResults(results.total);
      setSearchQuery('');
    } catch (error) {
      console.error('Category search failed:', error);
      alert('Search failed. Please try again.');
    }
    setLoading(false);
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      setLoading(true);
      setHasSearched(true);
      try {
        const results = await searchAPI.searchProducts({ q: searchQuery.trim() });
        setProducts(results.products);
        setTotalResults(results.total);
      } catch (error) {
        console.error('Search failed:', error);
        alert('Search failed. Please check your connection and try again.');
      }
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif' }}>
      {/* Hero Section */}
      <section className="hero-section">
        <div className="container">
          <h1 className="hero-title">
            AI-Powered Product Search Engine
          </h1>
          <p className="hero-subtitle">
            Find the best products at the most competitive prices across cosmetics, 
            fashion, and healthcare categories with intelligent search and price comparison.
          </p>
          
          <form onSubmit={handleSearch}>
            <input
              className="search-input"
              type="text"
              placeholder="Search for cosmetics, fashion, or healthcare products..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </form>
        </div>
      </section>

      {/* Categories Section */}
      <section style={{ padding: '2rem 0' }}>
        <div className="container">
          <h2 className="section-title">Shop by Category</h2>
          <div className="categories-grid">
            {categories.map((category) => (
              <div 
                key={category.id}
                className="category-card"
                onClick={() => handleCategoryClick(category.id)}
              >
                <div className="category-icon">{category.icon}</div>
                <h3 className="category-title">{category.title}</h3>
                <p className="category-description">{category.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Search Results Section */}
      {hasSearched && (
        <section style={{ padding: '2rem 0', backgroundColor: 'white' }}>
          <div className="container">
            <h2 className="section-title">
              {loading ? 'Searching...' : `Search Results (${totalResults} found)`}
            </h2>
            
            {loading && (
              <div style={{ textAlign: 'center', padding: '2rem' }}>
                <p>🔍 Searching for products...</p>
              </div>
            )}
            
            {!loading && products.length === 0 && (
              <div style={{ textAlign: 'center', padding: '2rem', color: '#64748b' }}>
                <p>No products found. Try a different search term.</p>
              </div>
            )}
            
            {!loading && products.length > 0 && (
              <div className="products-grid">
                {products.map((product) => (
                  <ProductCard key={product.id} product={product} />
                ))}
              </div>
            )}
          </div>
        </section>
      )}

      {/* Demo Section - Only show if no search has been performed */}
      {!hasSearched && (
        <section style={{ padding: '2rem 0', backgroundColor: 'white' }}>
          <div className="container">
            <h2 className="section-title">Get Started</h2>
            <div style={{ textAlign: 'center', color: '#64748b' }}>
              <p>🎉 Your AI Product Search Engine is ready!</p>
              <p>Try searching for "makeup", "skincare", or browse categories above.</p>
              <p>Backend API: <a href="https://ai-search-backend.dnash29.workers.dev/api/health" target="_blank" rel="noopener noreferrer">Live on Cloudflare Workers</a></p>
            </div>
          </div>
        </section>
      )}
    </div>
  );
};

export default App;