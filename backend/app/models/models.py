from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    category = Column(String(100), nullable=False, index=True)  # cosmetics, fashion, healthcare
    subcategory = Column(String(100), index=True)
    brand = Column(String(100), index=True)
    price = Column(Float, nullable=False, index=True)
    original_price = Column(Float)
    discount_percentage = Column(Float)
    rating = Column(Float, index=True)
    review_count = Column(Integer, default=0)
    image_url = Column(String(500))
    product_url = Column(String(500), nullable=False)
    source_website = Column(String(100), nullable=False, index=True)
    in_stock = Column(Boolean, default=True, index=True)
    features = Column(JSON)  # Store product features as JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False, index=True)
    reviewer_name = Column(String(100))
    rating = Column(Float, nullable=False)
    review_text = Column(Text)
    sentiment_score = Column(Float)  # AI-analyzed sentiment
    helpful_votes = Column(Integer, default=0)
    verified_purchase = Column(Boolean, default=False)
    review_date = Column(DateTime)
    source_website = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SearchQuery(Base):
    __tablename__ = "search_queries"
    
    id = Column(Integer, primary_key=True, index=True)
    query_text = Column(String(500), nullable=False)
    category_filter = Column(String(100))
    price_min = Column(Float)
    price_max = Column(Float)
    results_count = Column(Integer)
    user_ip = Column(String(45))  # For analytics
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PriceHistory(Base):
    __tablename__ = "price_history"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False, index=True)
    price = Column(Float, nullable=False)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())