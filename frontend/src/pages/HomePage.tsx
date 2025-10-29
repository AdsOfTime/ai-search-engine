import React, { useState } from 'react';

const HomePage: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');

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
    window.location.href = `/search?category=${categoryId}`;
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      window.location.href = `/search?q=${encodeURIComponent(searchQuery)}`;
    }
  };

  return (
    <div style={{ minHeight: '100vh' }}>
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

      {/* Demo Products Section */}
      <section style={{ padding: '2rem 0', backgroundColor: 'white' }}>
        <div className="container">
          <h2 className="section-title">Demo Products</h2>
          <div style={{ textAlign: 'center', color: '#64748b' }}>
            <p>Connect your backend API to display real products here.</p>
            <p>Backend API available at: <a href="http://localhost:8000/docs">http://localhost:8000/docs</a></p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;