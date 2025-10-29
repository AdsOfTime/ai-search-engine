-- Cloudflare D1 Database Schema for AI Search Engine
-- Run this with: wrangler d1 execute ai-search-db --file=cloudflare-d1-schema.sql

-- Products table with AI-optimized structure
CREATE TABLE IF NOT EXISTS products (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    brand TEXT,
    category TEXT NOT NULL,
    subcategory TEXT,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    original_price DECIMAL(10,2),
    rating DECIMAL(3,2),
    review_count INTEGER DEFAULT 0,
    image_url TEXT,
    additional_images TEXT, -- JSON array of image URLs
    in_stock BOOLEAN DEFAULT TRUE,
    stock_count INTEGER,
    features TEXT, -- JSON array of product features
    ingredients TEXT, -- JSON array for cosmetics/healthcare
    affiliate_links TEXT, -- JSON object with store URLs
    ai_tags TEXT, -- AI-generated tags for search
    ai_category_score DECIMAL(3,2), -- AI confidence in categorization
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Reviews table for sentiment analysis
CREATE TABLE IF NOT EXISTS reviews (
    id TEXT PRIMARY KEY,
    product_id TEXT NOT NULL,
    user_id TEXT,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT,
    review_title TEXT,
    verified_purchase BOOLEAN DEFAULT FALSE,
    helpful_count INTEGER DEFAULT 0,
    ai_sentiment_score DECIMAL(3,2), -- -1 to 1 sentiment score
    ai_sentiment_label TEXT, -- positive, negative, neutral
    ai_extracted_features TEXT, -- JSON array of mentioned features
    source_platform TEXT, -- Amazon, Sephora, etc.
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- User interactions for personalization
CREATE TABLE IF NOT EXISTS user_interactions (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    interaction_type TEXT CHECK (interaction_type IN ('view', 'click', 'purchase', 'wishlist', 'review')),
    session_id TEXT,
    search_query TEXT, -- What they searched for
    interaction_data TEXT, -- JSON with additional context
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Search queries for AI learning
CREATE TABLE IF NOT EXISTS search_queries (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    session_id TEXT,
    original_query TEXT NOT NULL,
    enhanced_query TEXT, -- AI-enhanced version
    search_intent TEXT, -- AI-detected intent
    filters_applied TEXT, -- JSON object
    results_count INTEGER,
    clicked_products TEXT, -- JSON array of product IDs
    search_duration INTEGER, -- milliseconds
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Categories for hierarchical organization
CREATE TABLE IF NOT EXISTS categories (
    id TEXT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    parent_id TEXT,
    description TEXT,
    ai_keywords TEXT, -- JSON array of AI-detected keywords
    display_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (parent_id) REFERENCES categories(id)
);

-- Brands information
CREATE TABLE IF NOT EXISTS brands (
    id TEXT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    logo_url TEXT,
    website_url TEXT,
    ai_reputation_score DECIMAL(3,2), -- AI-calculated brand reputation
    product_count INTEGER DEFAULT 0,
    average_rating DECIMAL(3,2),
    is_verified BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- AI model training data and performance
CREATE TABLE IF NOT EXISTS ai_model_metrics (
    id TEXT PRIMARY KEY,
    model_name TEXT NOT NULL,
    model_version TEXT,
    accuracy_score DECIMAL(5,4),
    training_date DATETIME,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
    performance_data TEXT, -- JSON with detailed metrics
    is_active BOOLEAN DEFAULT TRUE
);

-- Trending and recommendations cache
CREATE TABLE IF NOT EXISTS trending_products (
    id TEXT PRIMARY KEY,
    product_id TEXT NOT NULL,
    category TEXT,
    trending_score DECIMAL(5,2),
    trend_type TEXT, -- daily, weekly, monthly
    calculation_date DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Create indexes for performance optimization
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_products_brand ON products(brand);
CREATE INDEX IF NOT EXISTS idx_products_price ON products(price);
CREATE INDEX IF NOT EXISTS idx_products_rating ON products(rating DESC);
CREATE INDEX IF NOT EXISTS idx_products_in_stock ON products(in_stock);
CREATE INDEX IF NOT EXISTS idx_products_ai_tags ON products(ai_tags);

CREATE INDEX IF NOT EXISTS idx_reviews_product_id ON reviews(product_id);
CREATE INDEX IF NOT EXISTS idx_reviews_rating ON reviews(rating);
CREATE INDEX IF NOT EXISTS idx_reviews_sentiment ON reviews(ai_sentiment_score);

CREATE INDEX IF NOT EXISTS idx_user_interactions_user_id ON user_interactions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_interactions_product_id ON user_interactions(product_id);
CREATE INDEX IF NOT EXISTS idx_user_interactions_type ON user_interactions(interaction_type);

CREATE INDEX IF NOT EXISTS idx_search_queries_user_id ON search_queries(user_id);
CREATE INDEX IF NOT EXISTS idx_search_queries_created_at ON search_queries(created_at);

CREATE INDEX IF NOT EXISTS idx_trending_products_category ON trending_products(category);
CREATE INDEX IF NOT EXISTS idx_trending_products_score ON trending_products(trending_score DESC);

-- Insert sample categories
INSERT OR IGNORE INTO categories (id, name, description) VALUES 
('cat_makeup', 'Makeup', 'Cosmetics and beauty products'),
('cat_skincare', 'Skincare', 'Facial and body skincare products'),
('cat_fragrance', 'Fragrance', 'Perfumes and body sprays'),
('cat_haircare', 'Hair Care', 'Shampoos, conditioners, and styling products'),
('cat_fashion', 'Fashion', 'Clothing and accessories'),
('cat_shoes', 'Shoes', 'Footwear for all occasions'),
('cat_health', 'Health & Wellness', 'Supplements and health products');

-- Insert sample brands
INSERT OR IGNORE INTO brands (id, name, description, is_verified) VALUES 
('brand_fenty', 'Fenty Beauty', 'Rihanna''s inclusive beauty brand', TRUE),
('brand_rare', 'Rare Beauty', 'Selena Gomez''s mental health focused beauty brand', TRUE),
('brand_glossier', 'Glossier', 'Minimalist beauty and skincare', TRUE),
('brand_cerave', 'CeraVe', 'Dermatologist recommended skincare', TRUE),
('brand_nike', 'Nike', 'Athletic footwear and apparel', TRUE);

-- Create triggers for automatic timestamp updates
CREATE TRIGGER IF NOT EXISTS update_products_timestamp 
    AFTER UPDATE ON products
    BEGIN
        UPDATE products SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

-- Sample data insert script (run separately after schema)
-- You can populate this with your existing scraped data