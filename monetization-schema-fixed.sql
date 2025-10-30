-- Monetization Tables for AI Search Engine (Fixed)
-- Add these tables to your existing Cloudflare D1 database

-- Track affiliate clicks and revenue (no foreign key constraints)
CREATE TABLE IF NOT EXISTS affiliate_clicks (
    id TEXT PRIMARY KEY,
    product_id TEXT NOT NULL,
    user_id TEXT,
    retailer TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    revenue_potential REAL NOT NULL,
    ip_address TEXT,
    user_agent TEXT
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
    session_id TEXT
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
    status TEXT NOT NULL -- 'active', 'paused', 'ended'
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_affiliate_clicks_product ON affiliate_clicks(product_id);
CREATE INDEX IF NOT EXISTS idx_affiliate_clicks_timestamp ON affiliate_clicks(timestamp);
CREATE INDEX IF NOT EXISTS idx_user_interactions_user ON user_interactions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_interactions_product ON user_interactions(product_id);
CREATE INDEX IF NOT EXISTS idx_sponsored_products_active ON sponsored_products(status, start_date, end_date);
CREATE INDEX IF NOT EXISTS idx_revenue_events_timestamp ON revenue_events(timestamp);

-- Insert sample subscription plans
INSERT OR REPLACE INTO subscriptions (id, user_id, plan_type, status, created_at, expires_at, monthly_fee, features_enabled) VALUES
('sub_1', 'user_demo', 'pro', 'active', datetime('now'), datetime('now', '+1 month'), 9.99, '["advanced_search", "price_alerts", "unlimited_saves"]'),
('sub_2', 'user_business', 'business', 'active', datetime('now'), datetime('now', '+1 month'), 29.99, '["api_access", "bulk_data", "analytics_dashboard"]');

-- Insert sample sponsored products
INSERT OR REPLACE INTO sponsored_products (id, product_id, advertiser, campaign_name, bid_amount, daily_budget, start_date, end_date, target_keywords, status) VALUES
('sp_1', '1', 'Fenty Beauty', 'Holiday Campaign', 0.75, 50.00, date('now'), date('now', '+30 days'), '["foundation", "makeup", "beauty"]', 'active'),
('sp_2', '2', 'Rare Beauty', 'New Product Launch', 0.85, 75.00, date('now'), date('now', '+30 days'), '["blush", "cosmetics", "selena gomez"]', 'active');

-- Sample affiliate click data for analytics
INSERT OR REPLACE INTO affiliate_clicks (id, product_id, user_id, retailer, timestamp, revenue_potential, ip_address) VALUES
('click_1', '1', 'user_123', 'amazon', datetime('now', '-2 days'), 2.50, '192.168.1.1'),
('click_2', '2', 'user_456', 'sephora', datetime('now', '-1 day'), 3.25, '192.168.1.2'),
('click_3', '3', 'user_789', 'target', datetime('now'), 1.75, '192.168.1.3');

-- Sample revenue events
INSERT OR REPLACE INTO revenue_events (id, event_type, amount, currency, source, user_id, product_id, timestamp, metadata) VALUES
('rev_1', 'affiliate_commission', 2.50, 'USD', 'amazon', 'user_123', '1', datetime('now', '-2 days'), '{"order_id": "AMZ123456"}'),
('rev_2', 'subscription', 9.99, 'USD', 'subscription', 'user_demo', NULL, datetime('now', '-1 month'), '{"plan": "pro", "billing_cycle": "monthly"}'),
('rev_3', 'affiliate_commission', 3.25, 'USD', 'sephora', 'user_456', '2', datetime('now', '-1 day'), '{"order_id": "SEP789012"}');