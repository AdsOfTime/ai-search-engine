-- Sample data for AI Product Search Engine development

-- Insert sample categories
INSERT INTO products (name, description, category, subcategory, brand, price, original_price, rating, review_count, image_url, product_url, source_website, in_stock) VALUES 
-- Cosmetics
('Moisturizing Face Cream', 'Daily facial moisturizer with hyaluronic acid and ceramides for all skin types', 'cosmetics', 'skincare', 'CeraVe', 15.99, 19.99, 4.5, 1250, 'https://example.com/images/cerave-cream.jpg', 'https://example.com/products/cerave-cream', 'amazon.com', true),
('Waterproof Mascara', 'Long-lasting waterproof mascara for voluminous lashes', 'cosmetics', 'makeup', 'Maybelline', 8.99, null, 4.2, 850, 'https://example.com/images/maybelline-mascara.jpg', 'https://example.com/products/maybelline-mascara', 'ulta.com', true),
('Vitamin C Serum', 'Brightening vitamin C serum with 20% L-ascorbic acid', 'cosmetics', 'skincare', 'Skinceuticals', 165.00, null, 4.7, 2100, 'https://example.com/images/skinceuticals-serum.jpg', 'https://example.com/products/skinceuticals-serum', 'sephora.com', true),
('Matte Liquid Lipstick', 'Long-wearing matte liquid lipstick in Ruby Red', 'cosmetics', 'makeup', 'Fenty Beauty', 24.00, null, 4.3, 950, 'https://example.com/images/fenty-lipstick.jpg', 'https://example.com/products/fenty-lipstick', 'sephora.com', true),

-- Fashion
('Cotton T-Shirt', 'Premium 100% cotton t-shirt in navy blue', 'fashion', 'tops', 'Uniqlo', 12.90, 14.90, 4.1, 650, 'https://example.com/images/uniqlo-tshirt.jpg', 'https://example.com/products/uniqlo-tshirt', 'uniqlo.com', true),
('Denim Jeans', 'Classic straight-leg denim jeans in dark wash', 'fashion', 'bottoms', 'Levis', 79.50, 89.50, 4.4, 1200, 'https://example.com/images/levis-jeans.jpg', 'https://example.com/products/levis-jeans', 'levis.com', true),
('Running Shoes', 'Lightweight running shoes with air cushioning', 'fashion', 'shoes', 'Nike', 120.00, 140.00, 4.6, 2800, 'https://example.com/images/nike-shoes.jpg', 'https://example.com/products/nike-shoes', 'nike.com', true),
('Leather Handbag', 'Genuine leather crossbody handbag in black', 'fashion', 'accessories', 'Coach', 295.00, null, 4.8, 450, 'https://example.com/images/coach-handbag.jpg', 'https://example.com/products/coach-handbag', 'coach.com', true),

-- Healthcare
('Multivitamin Tablets', 'Daily multivitamin with essential vitamins and minerals', 'healthcare', 'supplements', 'Centrum', 19.99, 24.99, 4.2, 1800, 'https://example.com/images/centrum-multivitamin.jpg', 'https://example.com/products/centrum-multivitamin', 'cvs.com', true),
('Omega-3 Fish Oil', 'High-potency omega-3 fish oil capsules 1000mg', 'healthcare', 'supplements', 'Nordic Naturals', 45.95, null, 4.5, 920, 'https://example.com/images/nordic-omega3.jpg', 'https://example.com/products/nordic-omega3', 'walgreens.com', true),
('Pain Relief Cream', 'Topical pain relief cream with menthol and camphor', 'healthcare', 'pain relief', 'Aspercreme', 8.49, 9.99, 3.9, 340, 'https://example.com/images/aspercreme.jpg', 'https://example.com/products/aspercreme', 'cvs.com', true),
('Probiotic Supplement', 'Daily probiotic with 10 billion live cultures', 'healthcare', 'supplements', 'Garden of Life', 32.99, 39.99, 4.3, 760, 'https://example.com/images/garden-probiotic.jpg', 'https://example.com/products/garden-probiotic', 'vitacost.com', true);

-- Insert sample reviews
INSERT INTO reviews (product_id, reviewer_name, rating, review_text, sentiment_score, helpful_votes, verified_purchase, review_date, source_website) VALUES 
(1, 'Sarah M.', 5, 'This moisturizer is amazing! It absorbs quickly and keeps my skin hydrated all day. Perfect for sensitive skin.', 0.8, 15, true, '2024-01-15', 'amazon.com'),
(1, 'Mike R.', 4, 'Good product, nice texture. A bit pricey but works well for dry skin.', 0.4, 8, true, '2024-01-10', 'amazon.com'),
(2, 'Jessica L.', 5, 'Best mascara ever! Stays on all day and through workouts. No smudging at all.', 0.9, 22, true, '2024-01-20', 'ulta.com'),
(3, 'Dr. Amanda K.', 5, 'As a dermatologist, I recommend this serum. High quality vitamin C that really works for brightening.', 0.85, 45, true, '2024-01-18', 'sephora.com'),
(7, 'Running_Pro', 5, 'Excellent running shoes! Great cushioning and support. Perfect for long distance runs.', 0.8, 30, true, '2024-01-12', 'nike.com'),
(9, 'HealthyMom', 4, 'Good multivitamin with all essential nutrients. Easy to swallow and no aftertaste.', 0.6, 12, true, '2024-01-08', 'cvs.com');

-- Insert sample search queries for analytics
INSERT INTO search_queries (query_text, category_filter, results_count, user_ip) VALUES 
('moisturizer for dry skin', 'cosmetics', 45, '192.168.1.1'),
('running shoes nike', 'fashion', 23, '192.168.1.2'),
('vitamin c serum', 'cosmetics', 67, '192.168.1.3'),
('omega 3 supplements', 'healthcare', 34, '192.168.1.4'),
('waterproof mascara', 'cosmetics', 56, '192.168.1.5');

-- Insert sample price history
INSERT INTO price_history (product_id, price, recorded_at) VALUES 
(1, 19.99, '2024-01-01'),
(1, 17.99, '2024-01-10'),
(1, 15.99, '2024-01-20'),
(7, 140.00, '2024-01-01'),
(7, 130.00, '2024-01-15'),
(7, 120.00, '2024-01-20'),
(9, 24.99, '2024-01-01'),
(9, 22.99, '2024-01-10'),
(9, 19.99, '2024-01-20');