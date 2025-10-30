-- Monetization Tables for AI Search Engine
-- Add these tables to your existing Cloudflare D1 database

-- Track affiliate clicks and revenue
CREATE TABLE IF NOT EXISTS affiliate_clicks (
    id TEXT PRIMARY KEY,
    product_id TEXT NOT NULL,
    user_id TEXT,
    retailer TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    revenue_potential REAL NOT NULL,
    ip_address TEXT,
    user_agent TEXT,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- User subscriptions for premium features
CREATE TABLE IF NOT EXISTS subscriptions (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL UNIQUE,
    plan_type TEXT NOT NULL, -- 'basic', 'pro', 'business'
    status TEXT NOT NULL, -- 'active', 'cancelled', 'expired'
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    monthly_fee REAL NOT NULL,
    features_enabled TEXT NOT NULL -- JSON string of enabled features
);

-- Revenue tracking
CREATE TABLE IF NOT EXISTS revenue_events (
    id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL, -- 'affiliate_commission', 'subscription', 'ad_click'
    amount REAL NOT NULL,
    currency TEXT DEFAULT 'USD',
    source TEXT NOT NULL, -- retailer name or 'subscription' or 'advertising'
    user_id TEXT,
    product_id TEXT,
    timestamp TEXT NOT NULL,
    metadata TEXT -- JSON for additional data
);

-- User interactions for better recommendations
CREATE TABLE IF NOT EXISTS user_interactions (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    interaction_type TEXT NOT NULL, -- 'view', 'click', 'save', 'purchase'
    timestamp TEXT NOT NULL,
    session_id TEXT,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Sponsored product placements
CREATE TABLE IF NOT EXISTS sponsored_products (
    id TEXT PRIMARY KEY,
    product_id TEXT NOT NULL,
    advertiser TEXT NOT NULL,
    campaign_name TEXT NOT NULL,
    bid_amount REAL NOT NULL, -- Amount paid per click
    daily_budget REAL NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    target_keywords TEXT, -- JSON array of keywords
    status TEXT NOT NULL, -- 'active', 'paused', 'ended'
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Update products table to include monetization fields
-- (Run these ALTER statements if your products table already exists)
ALTER TABLE products ADD COLUMN commission_rate REAL DEFAULT 0.04;
ALTER TABLE products ADD COLUMN featured_placement INTEGER DEFAULT 0;
ALTER TABLE products ADD COLUMN sponsor_priority INTEGER DEFAULT 0;

-- Create indexes for performance
CREATE INDEX idx_affiliate_clicks_product ON affiliate_clicks(product_id);
CREATE INDEX idx_affiliate_clicks_timestamp ON affiliate_clicks(timestamp);
CREATE INDEX idx_user_interactions_user ON user_interactions(user_id);
CREATE INDEX idx_user_interactions_product ON user_interactions(product_id);
CREATE INDEX idx_sponsored_products_active ON sponsored_products(status, start_date, end_date);
CREATE INDEX idx_revenue_events_timestamp ON revenue_events(timestamp);

-- Insert sample subscription plans
INSERT OR REPLACE INTO subscriptions (id, user_id, plan_type, status, created_at, expires_at, monthly_fee, features_enabled) VALUES
('sub_1', 'user_demo', 'pro', 'active', datetime('now'), datetime('now', '+1 month'), 9.99, '["advanced_search", "price_alerts", "unlimited_saves"]'),
('sub_2', 'user_business', 'business', 'active', datetime('now'), datetime('now', '+1 month'), 29.99, '["api_access", "bulk_data", "analytics_dashboard"]');

-- Insert sample sponsored products (if you have products with these IDs)
INSERT OR REPLACE INTO sponsored_products (id, product_id, advertiser, campaign_name, bid_amount, daily_budget, start_date, end_date, target_keywords, status) VALUES
('sp_1', '1', 'Fenty Beauty', 'Holiday Campaign', 0.75, 50.00, date('now'), date('now', '+30 days'), '["foundation", "makeup", "beauty"]', 'active'),
('sp_2', '2', 'Rare Beauty', 'New Product Launch', 0.85, 75.00, date('now'), date('now', '+30 days'), '["blush", "cosmetics", "selena gomez"]', 'active');