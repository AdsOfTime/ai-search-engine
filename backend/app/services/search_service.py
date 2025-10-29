from sqlalchemy.orm import Session
from sqlalchemy import text, or_, and_
from typing import List, Optional
from app.models.models import Product, SearchQuery
import re

class SearchService:
    def __init__(self, db: Session):
        self.db = db
    
    async def search_products(
        self,
        query: str,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_rating: Optional[float] = None,
        sort_by: str = "relevance",
        page: int = 1,
        limit: int = 20
    ):
        """Search products with filters and sorting"""
        
        # Log search query for analytics
        search_log = SearchQuery(
            query_text=query,
            category_filter=category,
            price_min=min_price,
            price_max=max_price
        )
        self.db.add(search_log)
        
        # Build base query
        base_query = self.db.query(Product)
        
        # Apply filters
        filters = []
        
        # Text search in name and description
        if query and query.strip():
            search_terms = query.lower().split()
            for term in search_terms:
                filters.append(
                    or_(
                        Product.name.ilike(f"%{term}%"),
                        Product.description.ilike(f"%{term}%"),
                        Product.brand.ilike(f"%{term}%")
                    )
                )
        
        if category:
            filters.append(Product.category == category)
        
        if min_price is not None:
            filters.append(Product.price >= min_price)
        
        if max_price is not None:
            filters.append(Product.price <= max_price)
        
        if min_rating is not None:
            filters.append(Product.rating >= min_rating)
        
        # Only show in-stock products
        filters.append(Product.in_stock == True)
        
        if filters:
            base_query = base_query.filter(and_(*filters))
        
        # Apply sorting
        if sort_by == "price_low":
            base_query = base_query.order_by(Product.price.asc())
        elif sort_by == "price_high":
            base_query = base_query.order_by(Product.price.desc())
        elif sort_by == "rating":
            base_query = base_query.order_by(Product.rating.desc())
        else:  # relevance (default)
            # For now, sort by rating and review count
            base_query = base_query.order_by(
                Product.rating.desc(),
                Product.review_count.desc()
            )
        
        # Apply pagination
        offset = (page - 1) * limit
        products = base_query.offset(offset).limit(limit).all()
        total = base_query.count()
        
        # Update search query results count
        search_log.results_count = total
        self.db.commit()
        
        return {
            "products": [self._format_product(p) for p in products],
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit
        }
    
    async def get_suggestions(self, query: str) -> List[str]:
        """Get search suggestions based on query"""
        # Simple implementation - can be enhanced with AI
        suggestions = []
        
        # Find products with similar names
        similar_products = (
            self.db.query(Product.name)
            .filter(Product.name.ilike(f"%{query}%"))
            .distinct()
            .limit(5)
            .all()
        )
        
        suggestions.extend([p.name for p in similar_products])
        
        # Add some common search terms based on category
        common_terms = {
            "cosmetics": ["foundation", "lipstick", "mascara", "eyeshadow", "concealer"],
            "fashion": ["dress", "jeans", "shoes", "jacket", "accessories"],
            "healthcare": ["vitamins", "supplements", "skincare", "medication", "wellness"]
        }
        
        for category, terms in common_terms.items():
            for term in terms:
                if query.lower() in term.lower():
                    suggestions.append(term)
        
        return list(set(suggestions))[:10]  # Remove duplicates and limit
    
    async def get_trending_products(self, category: Optional[str], limit: int) -> List[Product]:
        """Get trending products based on search patterns and ratings"""
        query = self.db.query(Product).filter(Product.in_stock == True)
        
        if category:
            query = query.filter(Product.category == category)
        
        # Sort by rating and review count to simulate trending
        trending = (
            query.order_by(
                Product.rating.desc(),
                Product.review_count.desc(),
                Product.created_at.desc()
            )
            .limit(limit)
            .all()
        )
        
        return trending
    
    def _format_product(self, product: Product) -> dict:
        """Format product for API response"""
        return {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "category": product.category,
            "brand": product.brand,
            "price": float(product.price) if product.price else 0.0,
            "rating": float(product.rating) if product.rating else 0.0,
            "review_count": product.review_count if product.review_count else 0,
            "image_url": product.image_url,
            "product_url": product.product_url,
            "source_website": product.source_website,
            "in_stock": product.in_stock,
            "created_at": product.created_at.isoformat() if product.created_at else None
        }