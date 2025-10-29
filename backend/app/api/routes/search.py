from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.services.search_service import SearchService
from app.services.ai_service import AIService

router = APIRouter()

@router.get("/products")
async def search_products(
    q: Optional[str] = Query(None, description="Search query"),
    category: Optional[str] = Query(None, description="Product category filter"),
    min_price: Optional[float] = Query(None, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, description="Maximum price filter"),
    min_rating: Optional[float] = Query(None, description="Minimum rating filter"),
    sort_by: Optional[str] = Query("relevance", description="Sort by: relevance, price_low, price_high, rating"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Results per page"),
    db: Session = Depends(get_db)
):
    """Search for products using AI-powered search"""
    search_service = SearchService(db)
    ai_service = AIService()
    
    # Use AI to enhance search query if query is provided
    if q:
        enhanced_query = await ai_service.enhance_search_query(q, category)
    else:
        enhanced_query = ""  # Empty query for category-only searches
    
    # Perform the search
    results = await search_service.search_products(
        query=enhanced_query,
        category=category,
        min_price=min_price,
        max_price=max_price,
        min_rating=min_rating,
        sort_by=sort_by,
        page=page,
        limit=limit
    )
    
    return results

@router.get("/suggestions")
async def get_search_suggestions(
    q: str = Query(..., description="Partial search query"),
    db: Session = Depends(get_db)
):
    """Get AI-powered search suggestions"""
    search_service = SearchService(db)
    suggestions = await search_service.get_suggestions(q)
    return {"suggestions": suggestions}

@router.get("/trending")
async def get_trending_products(
    category: Optional[str] = Query(None, description="Product category"),
    limit: int = Query(10, ge=1, le=50, description="Number of trending products"),
    db: Session = Depends(get_db)
):
    """Get trending products based on search patterns and ratings"""
    search_service = SearchService(db)
    trending = await search_service.get_trending_products(category, limit)
    return {"trending_products": trending}