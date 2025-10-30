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
        <button 
          onClick={handleViewDetails}
          style={{
            marginTop: '0.75rem',
            padding: '0.5rem 1rem',
            backgroundColor: '#6366f1',
            color: 'white',
            border: 'none',
            borderRadius: '6px',
            fontSize: '0.875rem',
            cursor: 'pointer',
            width: '100%',
            transition: 'background-color 0.2s ease'
          }}
          onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#4f46e5'}
          onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#6366f1'}
        >
          View Details
        </button>
      </div>
    </div>
  );
};

export default ProductCard;