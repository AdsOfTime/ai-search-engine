-- Insert sample product data for testing
INSERT INTO products (id, name, brand, category, price, rating, description, in_stock, created_at) VALUES 
('1', 'Fenty Beauty Pro Filt''r Foundation', 'Fenty Beauty', 'makeup', 36.00, 4.5, 'Full coverage foundation with 50 shades for all skin tones', 1, datetime('now')),
('2', 'Rare Beauty Soft Pinch Liquid Blush', 'Rare Beauty', 'makeup', 20.00, 4.7, 'Weightless liquid blush that blends seamlessly', 1, datetime('now')),
('3', 'CeraVe Daily Moisturizing Lotion', 'CeraVe', 'skincare', 15.99, 4.6, 'Hydrating lotion with ceramides and hyaluronic acid', 1, datetime('now')),
('4', 'Glossier Cloud Paint Blush', 'Glossier', 'makeup', 18.00, 4.4, 'Seamless cheek color in a gel formula', 1, datetime('now')),
('5', 'The Ordinary Niacinamide Serum', 'The Ordinary', 'skincare', 7.20, 4.3, '10% Niacinamide + 1% Zinc serum for blemish-prone skin', 1, datetime('now')),
('6', 'Maybelline Sky High Mascara', 'Maybelline', 'makeup', 10.99, 4.2, 'Lengthening and volumizing mascara', 1, datetime('now')),
('7', 'Nike Air Force 1 Sneakers', 'Nike', 'shoes', 90.00, 4.5, 'Classic white leather sneakers', 1, datetime('now')),
('8', 'Levi''s 501 Original Jeans', 'Levi''s', 'fashion', 69.50, 4.3, 'Classic straight leg denim jeans', 1, datetime('now')),
('9', 'Nature Made Vitamin D3', 'Nature Made', 'supplements', 12.99, 4.6, '2000 IU Vitamin D3 for bone and immune support', 1, datetime('now')),
('10', 'Optimum Nutrition Whey Protein', 'Optimum Nutrition', 'supplements', 54.99, 4.7, 'Gold Standard 100% Whey Protein Powder', 1, datetime('now'));

-- Insert some sample reviews for sentiment analysis
INSERT INTO reviews (id, product_id, rating, review_text, ai_sentiment_score, ai_sentiment_label, created_at) VALUES
('r1', '1', 5, 'Amazing foundation! Perfect color match and long-lasting coverage.', 0.9, 'positive', datetime('now')),
('r2', '1', 4, 'Good coverage but can be a bit heavy for daily wear.', 0.3, 'neutral', datetime('now')),
('r3', '2', 5, 'Love this blush! The color is so natural and it lasts all day.', 0.8, 'positive', datetime('now')),
('r4', '3', 5, 'My holy grail moisturizer! Keeps my skin hydrated without being greasy.', 0.9, 'positive', datetime('now')),
('r5', '5', 4, 'Helps with my acne but takes time to see results.', 0.2, 'neutral', datetime('now'));