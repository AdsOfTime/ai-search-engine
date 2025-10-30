import React from 'react';
import { Product } from '../types/index';

interface ProductCardProps {
  product: Product;
}

const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
  const [imageError, setImageError] = React.useState(false);

  const handleViewDetails = (e: React.MouseEvent) => {
    e.stopPropagation();
    // Show product details in alert for now
    // TODO: Replace with proper modal or detail page
    alert(`${product.name}\n\n🏷️ Brand: ${product.brand}\n💰 Price: $${product.price}\n⭐ Rating: ${product.rating?.toFixed(1) || 'N/A'}/5 (${product.review_count || 0} reviews)\n📝 Category: ${product.category}\n\n${product.description || 'No description available'}`);
  };

  const handleBuyNow = async (retailer: string) => {
    try {
      // Track affiliate click for monetization
      const response = await fetch('https://ai-search-backend.dnash29.workers.dev/api/affiliate/click', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          product_id: product.id,
          retailer: retailer,
          user_id: localStorage.getItem('userId') || `anon_${Date.now()}`
        })
      });

      const data = await response.json();
      
      if (data.affiliate_url) {
        // Open affiliate link in new tab
        window.open(data.affiliate_url, '_blank');
      } else {
        // Fallback to generic product page
        const fallbackUrls = {
          amazon: `https://www.amazon.com/s?k=${encodeURIComponent(product.name)}`,
          sephora: `https://www.sephora.com/search?keyword=${encodeURIComponent(product.name)}`,
          target: `https://www.target.com/s?searchTerm=${encodeURIComponent(product.name)}`,
          cvs: `https://www.cvs.com/shop?searchTerm=${encodeURIComponent(product.name)}`
        };
        window.open(fallbackUrls[retailer as keyof typeof fallbackUrls] || '#', '_blank');
      }
    } catch (error) {
      console.error('Error tracking affiliate click:', error);
      // Still open a search page as fallback
      window.open(`https://www.google.com/search?q=${encodeURIComponent(product.name)} buy online`, '_blank');
    }
  };

  const handleImageError = () => {
    setImageError(true);
  };

  return (
    <div className="product-card">
      {imageError || !product.image_url ? (
        <div 
          className="product-image"
          style={{
            height: '200px',
            backgroundColor: '#f3f4f6',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '3rem',
            color: '#9ca3af'
          }}
        >
          🎨
        </div>
      ) : (
        <img 
          className="product-image"
          src={product.image_url} 
          alt={product.name}
          onError={handleImageError}
        />
      )}
      <div style={{ padding: '1rem' }}>
        <div className="product-brand">{product.brand}</div>
        <h3 className="product-name">{product.name}</h3>
        <div className="product-price">${product.price}</div>
        <div className="product-rating">
          ⭐ {product.rating?.toFixed(1) || 'N/A'} ({product.review_count || 0} reviews)
        </div>
        <div style={{ marginTop: '0.75rem' }}>
          <button 
            onClick={handleViewDetails}
            style={{
              padding: '0.5rem 1rem',
              backgroundColor: '#6366f1',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              fontSize: '0.875rem',
              cursor: 'pointer',
              width: '100%',
              marginBottom: '0.5rem',
              transition: 'background-color 0.2s ease'
            }}
            onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#4f46e5'}
            onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#6366f1'}
          >
            📋 View Details
          </button>
          
          <div style={{ display: 'flex', gap: '0.25rem' }}>
            <button 
              onClick={() => handleBuyNow('amazon')}
              style={{
                flex: 1,
                padding: '0.4rem 0.5rem',
                backgroundColor: '#ff9900',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                fontSize: '0.75rem',
                cursor: 'pointer',
                fontWeight: 'bold'
              }}
              title="Buy on Amazon (Affiliate Link)"
            >
              🛒 Amazon
            </button>
            
            <button 
              onClick={() => handleBuyNow('sephora')}
              style={{
                flex: 1,
                padding: '0.4rem 0.5rem',
                backgroundColor: '#000000',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                fontSize: '0.75rem',
                cursor: 'pointer',
                fontWeight: 'bold'
              }}
              title="Buy on Sephora (Affiliate Link)"
            >
              💄 Sephora
            </button>
            
            <button 
              onClick={() => handleBuyNow('target')}
              style={{
                flex: 1,
                padding: '0.4rem 0.5rem',
                backgroundColor: '#cc0000',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                fontSize: '0.75rem',
                cursor: 'pointer',
                fontWeight: 'bold'
              }}
              title="Buy on Target (Affiliate Link)"
            >
              🎯 Target
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;