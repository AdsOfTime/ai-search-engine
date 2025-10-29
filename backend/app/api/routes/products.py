from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import Product, Review

router = APIRouter()

@router.get("/{product_id}")
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get detailed product information"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get reviews for this product
    reviews = db.query(Review).filter(Review.product_id == product_id).limit(10).all()
    
    return {
        "product": product,
        "reviews": reviews
    }

@router.get("/{product_id}/reviews")
async def get_product_reviews(
    product_id: int, 
    page: int = 1, 
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get reviews for a specific product"""
    offset = (page - 1) * limit
    reviews = (
        db.query(Review)
        .filter(Review.product_id == product_id)
        .offset(offset)
        .limit(limit)
        .all()
    )
    
    total_reviews = db.query(Review).filter(Review.product_id == product_id).count()
    
    return {
        "reviews": reviews,
        "total": total_reviews,
        "page": page,
        "limit": limit
    }

@router.get("/{product_id}/price-history")
async def get_price_history(product_id: int, db: Session = Depends(get_db)):
    """Get price history for a product"""
    from app.models.models import PriceHistory
    
    price_history = (
        db.query(PriceHistory)
        .filter(PriceHistory.product_id == product_id)
        .order_by(PriceHistory.recorded_at.desc())
        .limit(30)
        .all()
    )
    
    return {"price_history": price_history}

@router.get("/{product_id}/similar")
async def get_similar_products(product_id: int, limit: int = 10, db: Session = Depends(get_db)):
    """Get similar products using AI similarity matching"""
    from app.services.ai_service import AIService
    
    # Get the target product
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Use AI service to find similar products
    ai_service = AIService()
    similar_products = await ai_service.find_similar_products(product, limit, db)
    
    return {"similar_products": similar_products}