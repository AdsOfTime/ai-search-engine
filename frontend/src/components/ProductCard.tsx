import React from 'react';
import { Product } from '../types/index';

interface ProductCardProps {
  product: Product;
}

const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
  const handleClick = () => {
    // Navigate to product detail page
    window.location.href = `/product/${product.id}`;
  };

  return (
    <div className="product-card" onClick={handleClick}>
      <img 
        className="product-image"
        src={product.image_url || '/placeholder-product.jpg'} 
        alt={product.name}
      />
      <div style={{ padding: '1rem' }}>
        <div className="product-brand">{product.brand}</div>
        <h3 className="product-name">{product.name}</h3>
        <div className="product-price">${product.price}</div>
        <div className="product-rating">
          ⭐ {product.rating?.toFixed(1) || 'N/A'} ({product.review_count || 0} reviews)
        </div>
      </div>
    </div>
  );
};

export default ProductCard;