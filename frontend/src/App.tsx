import React from 'react';
import './App.css';

const App: React.FC = () => {
  const [searchQuery, setSearchQuery] = React.useState('');

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

  const handleCategoryClick = (categoryId: string) => {
    alert(`Searching for ${categoryId} products...`);
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      alert(`Searching for: ${searchQuery}`);
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

      {/* Demo Section */}
      <section style={{ padding: '2rem 0', backgroundColor: 'white' }}>
        <div className="container">
          <h2 className="section-title">Demo Products</h2>
          <div style={{ textAlign: 'center', color: '#64748b' }}>
            <p>🎉 Your AI Product Search Engine is running!</p>
            <p>Backend API available at: <a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer">http://localhost:8000/docs</a></p>
            <p>Start building your product database and AI features.</p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default App;