#!/usr/bin/env python3
"""
Advanced Multi-API Product Scraper
Fetch products from multiple APIs and add to database
"""

import asyncio
import aiohttp
import json
from typing import List, Dict
from sqlalchemy.orm import sessionmaker
from app.core.database import engine
from app.models.models import Product
from api_directory import MultiAPIProductScraper, ProductAPIDirectory
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedProductScraper:
    def __init__(self):
        self.Session = sessionmaker(bind=engine)
        self.directory = ProductAPIDirectory()
        self.scraper = None
        
    async def scrape_all_free_apis(self, limits: Dict[str, int] = None):
        """Scrape products from all free APIs"""
        if not limits:
            limits = {
                'makeup': 25,
                'platzi': 20, 
                'fda': 15,
                'usda': 10,
                'dummyjson': 30,
                'fakestore': 15
            }
        
        all_products = []
        
        async with MultiAPIProductScraper() as scraper:
            self.scraper = scraper
            
            # Cosmetics APIs
            makeup_products = await scraper.fetch_makeup_products(limits.get('makeup', 25))
            all_products.extend(makeup_products)
            
            # Fashion APIs
            platzi_products = await scraper.fetch_platzi_products(limits.get('platzi', 20))
            all_products.extend(platzi_products)
            
            fakestore_products = await self.fetch_fakestore_api(limits.get('fakestore', 15))
            all_products.extend(fakestore_products)
            
            # Healthcare APIs
            fda_products = await scraper.fetch_fda_supplements(limits.get('fda', 15))
            all_products.extend(fda_products)
            
            usda_products = await scraper.fetch_usda_nutrition(limits.get('usda', 10))
            all_products.extend(usda_products)
            
            # General product APIs
            dummyjson_products = await self.fetch_dummyjson_categories(limits.get('dummyjson', 30))
            all_products.extend(dummyjson_products)
            
        logger.info(f"Total products scraped: {len(all_products)}")
        return all_products
    
    async def fetch_fakestore_api(self, limit: int = 15) -> List[Dict]:
        """Fetch from FakeStore API"""
        try:
            url = "https://fakestoreapi.com/products"
            async with self.scraper.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    products = []
                    
                    for item in data[:limit]:
                        # Map categories
                        category_mapping = {
                            "men's clothing": "fashion",
                            "women's clothing": "fashion", 
                            "jewelery": "fashion",
                            "electronics": "electronics"
                        }
                        
                        category = category_mapping.get(item.get('category', ''), 'fashion')
                        
                        product = {
                            'name': item.get('title', 'Unknown Product'),
                            'brand': 'FakeStore Brand',
                            'price': float(item.get('price', 0)),
                            'category': category,
                            'description': item.get('description', ''),
                            'rating': float(item.get('rating', {}).get('rate', 4.0)),
                            'review_count': int(item.get('rating', {}).get('count', 100)),
                            'image_url': item.get('image', ''),
                            'product_url': f"https://fakestoreapi.com/products/{item.get('id', '')}",
                            'source_website': 'fakestoreapi.com',
                            'in_stock': True
                        }
                        products.append(product)
                    
                    logger.info(f"Fetched {len(products)} FakeStore products")
                    return products
        except Exception as e:
            logger.error(f"FakeStore API error: {e}")
        return []
    
    async def fetch_dummyjson_categories(self, limit: int = 30) -> List[Dict]:
        """Fetch specific categories from DummyJSON"""
        try:
            # Fetch specific categories relevant to our niches
            categories = ['beauty', 'fragrances', 'mens-shirts', 'womens-dresses', 'womens-shoes']
            products = []
            
            for category in categories:
                if len(products) >= limit:
                    break
                    
                url = f"https://dummyjson.com/products/category/{category}"
                async with self.scraper.session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        for item in data.get('products', []):
                            if len(products) >= limit:
                                break
                                
                            # Map DummyJSON categories to our categories
                            category_mapping = {
                                'beauty': 'cosmetics',
                                'fragrances': 'cosmetics',
                                'mens-shirts': 'fashion',
                                'womens-dresses': 'fashion',
                                'womens-shoes': 'fashion'
                            }
                            
                            mapped_category = category_mapping.get(category, 'fashion')
                            
                            product = {
                                'name': item.get('title', 'Unknown Product'),
                                'brand': item.get('brand', 'DummyJSON Brand'),
                                'price': float(item.get('price', 0)),
                                'category': mapped_category,
                                'description': item.get('description', ''),
                                'rating': float(item.get('rating', 4.0)),
                                'review_count': item.get('stock', 100),
                                'image_url': item.get('thumbnail', ''),
                                'product_url': f"https://dummyjson.com/products/{item.get('id', '')}",
                                'source_website': 'dummyjson.com',
                                'in_stock': item.get('stock', 0) > 0
                            }
                            products.append(product)
                
                await asyncio.sleep(0.2)  # Rate limiting
            
            logger.info(f"Fetched {len(products)} DummyJSON products")
            return products
            
        except Exception as e:
            logger.error(f"DummyJSON API error: {e}")
        return []
    
    async def fetch_supplemental_apis(self) -> List[Dict]:
        """Fetch from additional free APIs"""
        products = []
        
        try:
            # JSONPlaceholder for mock data
            url = "https://jsonplaceholder.typicode.com/posts"
            async with self.scraper.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Convert posts to product-like data
                    for i, item in enumerate(data[:10]):
                        product = {
                            'name': f"Health Product {item.get('id', i)}",
                            'brand': 'WellBeing Co',
                            'price': round(15.99 + (i * 2.5), 2),
                            'category': 'healthcare',
                            'description': item.get('body', '')[:100] + '...',
                            'rating': round(4.0 + (i % 8) * 0.1, 1),
                            'review_count': 50 + (i * 10),
                            'image_url': f"https://via.placeholder.com/300x300?text=Health+Product+{i}",
                            'product_url': 'https://jsonplaceholder.typicode.com/',
                            'source_website': 'jsonplaceholder.typicode.com',
                            'in_stock': True
                        }
                        products.append(product)
                        
        except Exception as e:
            logger.error(f"Supplemental API error: {e}")
        
        return products
    
    def save_products_to_db(self, products: List[Dict]) -> int:
        """Save products to database with duplicate checking"""
        if not products:
            return 0
        
        session = self.Session()
        saved_count = 0
        
        try:
            for product_data in products:
                # Check for duplicates by name and brand
                existing = session.query(Product).filter(
                    Product.name == product_data['name'],
                    Product.brand == product_data['brand']
                ).first()
                
                if not existing:
                    product = Product(
                        name=product_data['name'],
                        brand=product_data['brand'],
                        price=product_data['price'],
                        category=product_data['category'],
                        description=product_data['description'],
                        rating=product_data['rating'],
                        review_count=product_data['review_count'],
                        image_url=product_data['image_url'],
                        product_url=product_data['product_url'],
                        source_website=product_data['source_website'],
                        in_stock=product_data['in_stock']
                    )
                    session.add(product)
                    saved_count += 1
            
            session.commit()
            logger.info(f"Saved {saved_count} new products to database")
            
        except Exception as e:
            session.rollback()
            logger.error(f"Database error: {e}")
        finally:
            session.close()
            
        return saved_count
    
    def generate_report(self, products: List[Dict]) -> Dict:
        """Generate scraping report"""
        if not products:
            return {"error": "No products to analyze"}
        
        # Analyze by category
        categories = {}
        sources = {}
        price_ranges = {'under_25': 0, '25_50': 0, '50_100': 0, 'over_100': 0}
        
        for product in products:
            # Categories
            cat = product.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
            
            # Sources
            source = product.get('source_website', 'unknown')
            sources[source] = sources.get(source, 0) + 1
            
            # Price ranges
            price = float(product.get('price', 0))
            if price < 25:
                price_ranges['under_25'] += 1
            elif price < 50:
                price_ranges['25_50'] += 1
            elif price < 100:
                price_ranges['50_100'] += 1
            else:
                price_ranges['over_100'] += 1
        
        avg_price = sum(float(p.get('price', 0)) for p in products) / len(products)
        avg_rating = sum(float(p.get('rating', 0)) for p in products) / len(products)
        
        return {
            'total_products': len(products),
            'categories': categories,
            'sources': sources,
            'price_analysis': {
                'average_price': round(avg_price, 2),
                'price_ranges': price_ranges
            },
            'quality_metrics': {
                'average_rating': round(avg_rating, 2),
                'products_with_images': sum(1 for p in products if p.get('image_url')),
                'products_with_descriptions': sum(1 for p in products if p.get('description'))
            }
        }

async def main():
    """Main scraping function"""
    scraper = AdvancedProductScraper()
    
    print("🚀 Starting Advanced Multi-API Product Scraping")
    print("=" * 60)
    
    # Define limits for each API
    limits = {
        'makeup': 30,      # Makeup API
        'platzi': 25,      # Platzi fake store  
        'fakestore': 20,   # FakeStore API
        'fda': 10,         # FDA supplements
        'usda': 10,        # USDA nutrition
        'dummyjson': 35    # DummyJSON categories
    }
    
    # Scrape all products
    start_time = datetime.now()
    all_products = await scraper.scrape_all_free_apis(limits)
    
    # Add supplemental data
    supplemental_products = await scraper.fetch_supplemental_apis()
    all_products.extend(supplemental_products)
    
    end_time = datetime.now()
    
    # Generate report
    report = scraper.generate_report(all_products)
    
    # Save to database
    saved_count = scraper.save_products_to_db(all_products)
    
    # Print results
    print(f"\n📊 SCRAPING REPORT")
    print(f"⏱️  Time taken: {end_time - start_time}")
    print(f"📦 Products scraped: {report['total_products']}")
    print(f"💾 Products saved: {saved_count}")
    print(f"💰 Average price: ${report['price_analysis']['average_price']}")
    print(f"⭐ Average rating: {report['quality_metrics']['average_rating']}")
    
    print(f"\n📂 Categories:")
    for cat, count in report['categories'].items():
        print(f"  - {cat.title()}: {count} products")
    
    print(f"\n🌐 Sources:")
    for source, count in report['sources'].items():
        print(f"  - {source}: {count} products")
    
    print(f"\n💸 Price Distribution:")
    for range_name, count in report['price_analysis']['price_ranges'].items():
        print(f"  - {range_name.replace('_', '-')}: {count} products")

if __name__ == "__main__":
    asyncio.run(main())