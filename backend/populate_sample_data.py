#!/usr/bin/env python3
"""
Sample Product Data Generator for AI Product Search Engine
Generates realistic sample data for cosmetics, fashion, and healthcare products
"""

import asyncio
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from app.core.database import engine
from app.models.models import Product, Review, SearchQuery, PriceHistory

# Sample data for product generation
COSMETICS_DATA = {
    'brands': ['L\'Oreal', 'MAC', 'Maybelline', 'Revlon', 'NARS', 'Urban Decay', 'Too Faced', 'Fenty Beauty', 'Rare Beauty', 'Charlotte Tilbury'],
    'products': [
        'Foundation', 'Concealer', 'Lipstick', 'Mascara', 'Eyeshadow Palette', 'Blush', 'Highlighter', 
        'Eyeliner', 'Lip Gloss', 'Primer', 'Setting Spray', 'Bronzer', 'Lip Balm', 'Face Mask'
    ],
    'descriptors': ['Matte', 'Dewy', 'Long-lasting', 'Waterproof', 'Natural', 'Glowing', 'Buildable', 'Creamy', 'Shimmer', 'Velvet']
}

FASHION_DATA = {
    'brands': ['Nike', 'Adidas', 'Zara', 'H&M', 'Forever 21', 'ASOS', 'Urban Outfitters', 'Gap', 'Levi\'s', 'Calvin Klein'],
    'products': [
        'T-Shirt', 'Jeans', 'Dress', 'Sweater', 'Jacket', 'Sneakers', 'Boots', 'Handbag', 
        'Scarf', 'Sunglasses', 'Watch', 'Belt', 'Hoodie', 'Skirt', 'Pants'
    ],
    'descriptors': ['Casual', 'Elegant', 'Sporty', 'Vintage', 'Modern', 'Classic', 'Trendy', 'Comfortable', 'Stylish', 'Chic']
}

HEALTHCARE_DATA = {
    'brands': ['Nature Made', 'Centrum', 'Garden of Life', 'NOW Foods', 'Optimum Nutrition', 'Nordic Naturals', 'Life Extension', 'Thorne', 'Pure Encapsulations', 'Solgar'],
    'products': [
        'Multivitamin', 'Vitamin D3', 'Omega-3', 'Probiotics', 'Magnesium', 'Vitamin C', 
        'B-Complex', 'Calcium', 'Zinc', 'Iron', 'Biotin', 'Turmeric', 'Collagen', 'CoQ10'
    ],
    'descriptors': ['Natural', 'Organic', 'Non-GMO', 'Gluten-Free', 'High Potency', 'Sustained Release', 'Extra Strength', 'Daily', 'Advanced Formula', 'Pure']
}

WEBSITES = ['amazon.com', 'sephora.com', 'ulta.com', 'target.com', 'walmart.com', 'cvs.com', 'walgreens.com']

class SampleDataGenerator:
    def __init__(self):
        self.Session = sessionmaker(bind=engine)
    
    def generate_product_name(self, category: str) -> tuple:
        """Generate a realistic product name and brand"""
        if category == 'cosmetics':
            data = COSMETICS_DATA
        elif category == 'fashion':
            data = FASHION_DATA
        else:  # healthcare
            data = HEALTHCARE_DATA
        
        brand = random.choice(data['brands'])
        product = random.choice(data['products'])
        descriptor = random.choice(data['descriptors'])
        
        # Generate different name patterns
        patterns = [
            f"{brand} {descriptor} {product}",
            f"{brand} {product} - {descriptor}",
            f"{descriptor} {product} by {brand}",
            f"{brand} Professional {product}"
        ]
        
        name = random.choice(patterns)
        return name, brand
    
    def generate_description(self, name: str, category: str) -> str:
        """Generate a product description"""
        base_descriptions = {
            'cosmetics': [
                "Experience long-lasting, beautiful coverage with this premium formula.",
                "Achieve a flawless, natural look with buildable coverage.",
                "Professional-quality makeup for everyday elegance.",
                "Dermatologist-tested and suitable for all skin types."
            ],
            'fashion': [
                "Comfortable and stylish design for modern lifestyle.",
                "Premium quality materials with attention to detail.",
                "Versatile piece that complements any wardrobe.",
                "Fashion-forward design with classic appeal."
            ],
            'healthcare': [
                "Supports overall health and wellness with natural ingredients.",
                "High-quality supplement manufactured to strict standards.",
                "Scientifically formulated for optimal absorption and effectiveness.",
                "Third-party tested for purity and potency."
            ]
        }
        
        return random.choice(base_descriptions[category])
    
    def generate_reviews(self, product_id: int, count: int = None) -> list:
        """Generate sample reviews for a product"""
        if count is None:
            count = random.randint(5, 50)
        
        review_templates = [
            ("Amazing product! Really works as advertised.", 5),
            ("Good quality but a bit expensive.", 4),
            ("Love this! Will definitely buy again.", 5),
            ("Decent product, does what it says.", 4),
            ("Not bad but there are better options.", 3),
            ("Excellent value for money!", 5),
            ("Works well, very satisfied with purchase.", 4),
            ("Good product, fast shipping.", 4),
            ("Quality could be better for the price.", 3),
            ("Outstanding! Exceeded my expectations.", 5)
        ]
        
        reviews = []
        for _ in range(count):
            text, rating = random.choice(review_templates)
            
            # Add some variation to review text
            variations = [
                text,
                text + " Highly recommend!",
                text + " Great customer service too.",
                text + " Fast delivery.",
                "Really impressed. " + text
            ]
            
            review_data = {
                'product_id': product_id,
                'reviewer_name': f"Customer{random.randint(1000, 9999)}",
                'rating': rating,
                'review_text': random.choice(variations),
                'sentiment_score': (rating - 3) / 2,  # Convert 1-5 to -1 to 1
                'verified_purchase': random.choice([True, False]),
                'helpful_votes': random.randint(0, 20),
                'source_website': random.choice(WEBSITES),
                'review_date': datetime.now() - timedelta(days=random.randint(1, 365)),
                'created_at': datetime.now() - timedelta(days=random.randint(1, 365))
            }
            reviews.append(review_data)
        
        return reviews
    
    def generate_price_history(self, product_id: int, current_price: float) -> list:
        """Generate price history for a product"""
        history = []
        base_price = current_price
        
        # Generate 10-20 historical price points
        for i in range(random.randint(10, 20)):
            # Vary price by ±20%
            variation = random.uniform(0.8, 1.2)
            price = round(base_price * variation, 2)
            
            history_entry = {
                'product_id': product_id,
                'price': price,
                'recorded_at': datetime.now() - timedelta(days=random.randint(1, 180))
            }
            history.append(history_entry)
        
        return history
    
    async def populate_products(self, count_per_category: int = 50):
        """Generate and save sample products to database"""
        session = self.Session()
        
        try:
            categories = ['cosmetics', 'fashion', 'healthcare']
            
            for category in categories:
                print(f"Generating {count_per_category} {category} products...")
                
                for i in range(count_per_category):
                    # Generate product data
                    name, brand = self.generate_product_name(category)
                    
                    product_data = {
                        'name': name,
                        'description': self.generate_description(name, category),
                        'category': category,
                        'brand': brand,
                        'price': round(random.uniform(5.0, 200.0), 2),
                        'rating': round(random.uniform(3.0, 5.0), 1),
                        'review_count': random.randint(10, 500),
                        'image_url': f"https://example.com/images/{category}_{i+1}.jpg",
                        'product_url': f"https://{random.choice(WEBSITES)}/product/{i+1}",
                        'source_website': random.choice(WEBSITES),
                        'in_stock': random.choice([True, True, True, False])  # 75% in stock
                    }
                    
                    # Create and save product
                    product = Product(**product_data)
                    session.add(product)
                    session.flush()  # Get the product ID
                    
                    # Generate reviews
                    reviews_data = self.generate_reviews(product.id)
                    for review_data in reviews_data:
                        review = Review(**review_data)
                        session.add(review)
                    
                    # Generate price history
                    price_history_data = self.generate_price_history(product.id, product.price)
                    for history_data in price_history_data:
                        price_history = PriceHistory(**history_data)
                        session.add(price_history)
                    
                    if (i + 1) % 10 == 0:
                        print(f"  Generated {i + 1}/{count_per_category} products")
            
            # Generate some sample search queries
            sample_queries = [
                "red lipstick", "anti-aging serum", "running shoes", "vitamin d", 
                "mascara waterproof", "winter coat", "protein powder", "face moisturizer",
                "jeans", "omega 3", "foundation", "handbag", "multivitamin", "blush"
            ]
            
            for query in sample_queries:
                search_query = SearchQuery(
                    query_text=query,
                    results_count=random.randint(5, 50),
                    user_ip="127.0.0.1",
                    created_at=datetime.now() - timedelta(days=random.randint(1, 30))
                )
                session.add(search_query)
            
            session.commit()
            
            total_products = count_per_category * len(categories)
            print(f"✅ Successfully generated {total_products} products with reviews and price history!")
            print(f"✅ Added {len(sample_queries)} sample search queries")
            
        except Exception as e:
            print(f"❌ Error generating sample data: {e}")
            session.rollback()
            raise
        
        finally:
            session.close()

async def main():
    """Main function to populate sample data"""
    print("🚀 AI Product Search Engine - Sample Data Generator")
    print("=" * 50)
    
    generator = SampleDataGenerator()
    
    # Generate 30 products per category (90 total)
    await generator.populate_products(count_per_category=30)
    
    print("\n🎉 Sample data generation complete!")
    print("\nYou now have:")
    print("• 90 sample products (30 each: cosmetics, fashion, healthcare)")
    print("• Hundreds of sample reviews with sentiment analysis")
    print("• Price history data for trend analysis")
    print("• Sample search queries for analytics")

if __name__ == "__main__":
    asyncio.run(main())