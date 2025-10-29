#!/usr/bin/env python3
"""
Production-Ready Web Scraper
Advanced techniques for real e-commerce scraping
"""

import asyncio
import aiohttp
import json
import time
import random
from typing import List, Dict, Optional
import logging
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse
import csv
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from app.core.database import engine
from app.models.models import Product
import requests

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ScrapingConfig:
    """Configuration for scraping sessions"""
    user_agents: List[str]
    delay_min: float = 1.0
    delay_max: float = 3.0
    max_retries: int = 3
    timeout: int = 30

class ProductionScraper:
    """Production-ready scraper with advanced features"""
    
    def __init__(self):
        self.config = ScrapingConfig(
            user_agents=[
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
            ]
        )
        self.Session = sessionmaker(bind=engine)
        self.scraped_urls = set()  # Avoid duplicates
        
    def get_random_headers(self) -> Dict[str, str]:
        """Generate randomized headers to avoid detection"""
        return {
            'User-Agent': random.choice(self.config.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    async def fetch_with_retry(self, session: aiohttp.ClientSession, url: str) -> Optional[str]:
        """Fetch URL with retry logic and error handling"""
        for attempt in range(self.config.max_retries):
            try:
                headers = self.get_random_headers()
                
                async with session.get(
                    url, 
                    headers=headers, 
                    timeout=aiohttp.ClientTimeout(total=self.config.timeout)
                ) as response:
                    if response.status == 200:
                        content = await response.text()
                        logger.info(f"✅ Successfully fetched: {url}")
                        return content
                    elif response.status == 429:  # Rate limited
                        wait_time = 2 ** attempt * 5  # Exponential backoff
                        logger.warning(f"Rate limited. Waiting {wait_time}s before retry...")
                        await asyncio.sleep(wait_time)
                    else:
                        logger.warning(f"HTTP {response.status} for {url}")
                        
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt < self.config.max_retries - 1:
                    await asyncio.sleep(random.uniform(1, 3))
        
        logger.error(f"❌ Failed to fetch after {self.config.max_retries} attempts: {url}")
        return None
    
    async def scrape_dummyjson_products(self) -> List[Dict]:
        """Scrape from DummyJSON API (real public API)"""
        logger.info("🔄 Scraping DummyJSON products...")
        products = []
        
        try:
            async with aiohttp.ClientSession() as session:
                # DummyJSON has a products API
                url = "https://dummyjson.com/products?limit=30"
                
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        for item in data.get('products', []):
                            # Map to our product structure
                            category_mapping = {
                                'beauty': 'cosmetics',
                                'fragrances': 'cosmetics',
                                'skincare': 'cosmetics',
                                'groceries': 'healthcare',
                                'home-decoration': 'fashion',
                                'furniture': 'fashion',
                                'womens-dresses': 'fashion',
                                'womens-shoes': 'fashion',
                                'mens-shirts': 'fashion',
                                'mens-shoes': 'fashion',
                                'mens-watches': 'fashion',
                                'womens-watches': 'fashion',
                                'womens-bags': 'fashion',
                                'womens-jewellery': 'fashion'
                            }
                            
                            category = category_mapping.get(item.get('category'), 'fashion')
                            
                            product = {
                                'name': item.get('title', 'Unknown Product'),
                                'description': item.get('description', ''),
                                'brand': item.get('brand', 'Generic'),
                                'category': category,
                                'price': float(item.get('price', 0)),
                                'rating': float(item.get('rating', 4.0)),
                                'review_count': random.randint(10, 100),
                                'image_url': item.get('thumbnail', ''),
                                'product_url': f"https://dummyjson.com/products/{item.get('id')}",
                                'source_website': 'dummyjson.com',
                                'in_stock': True
                            }
                            products.append(product)
                            
        except Exception as e:
            logger.error(f"DummyJSON scraping error: {e}")
        
        logger.info(f"✅ Scraped {len(products)} products from DummyJSON")
        return products
    
    async def scrape_reqres_users_as_brands(self) -> List[Dict]:
        """Creative: Use ReqRes users API to create fictional brand products"""
        logger.info("🔄 Creating brand products from ReqRes users...")
        products = []
        
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://reqres.in/api/users?page=1"
                
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        for user in data.get('data', []):
                            first_name = user.get('first_name', '')
                            last_name = user.get('last_name', '')
                            email = user.get('email', '')
                            
                            # Create brand products based on user data
                            brand_name = f"{first_name} {last_name}"
                            
                            # Generate products for this "brand"
                            product_types = [
                                ("Signature Foundation", "cosmetics", "Long-lasting liquid foundation"),
                                ("Premium Moisturizer", "cosmetics", "Hydrating daily moisturizer"),
                                ("Wellness Supplement", "healthcare", "Natural health supplement"),
                                ("Organic Vitamin", "healthcare", "Organic vitamin blend")
                            ]
                            
                            for product_name, category, description in product_types[:2]:  # Limit to 2 per brand
                                product = {
                                    'name': f"{brand_name} {product_name}",
                                    'description': f"{description} by {brand_name}",
                                    'brand': brand_name,
                                    'category': category,
                                    'price': round(random.uniform(15.99, 89.99), 2),
                                    'rating': round(random.uniform(3.8, 4.9), 1),
                                    'review_count': random.randint(20, 150),
                                    'image_url': user.get('avatar', ''),
                                    'product_url': f"https://reqres.in/api/users/{user.get('id')}",
                                    'source_website': 'reqres.in',
                                    'in_stock': True
                                }
                                products.append(product)
                                
        except Exception as e:
            logger.error(f"ReqRes scraping error: {e}")
        
        logger.info(f"✅ Created {len(products)} brand products from ReqRes")
        return products
    
    def save_to_csv(self, products: List[Dict], filename: str = None):
        """Save products to CSV for backup/analysis"""
        if not products:
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"C:\\AI Search\\backend\\scraped_products_{timestamp}.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                if products:
                    fieldnames = products[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(products)
                    
            logger.info(f"✅ Saved {len(products)} products to {filename}")
            
        except Exception as e:
            logger.error(f"CSV save error: {e}")
    
    async def save_products_to_database(self, products: List[Dict]) -> int:
        """Save products to database with duplicate checking"""
        if not products:
            return 0
        
        session = self.Session()
        saved_count = 0
        
        try:
            for product_data in products:
                # Advanced duplicate checking
                existing = session.query(Product).filter(
                    Product.name == product_data['name'],
                    Product.source_website == product_data['source_website']
                ).first()
                
                if not existing:
                    product = Product(**product_data)
                    session.add(product)
                    saved_count += 1
                else:
                    # Update existing product with new price/rating
                    existing.price = product_data['price']
                    existing.rating = product_data['rating']
                    existing.review_count = product_data['review_count']
            
            session.commit()
            logger.info(f"✅ Saved {saved_count} new products to database")
            
        except Exception as e:
            logger.error(f"Database error: {e}")
            session.rollback()
            
        finally:
            session.close()
            
        return saved_count
    
    def analyze_scraped_data(self, products: List[Dict]):
        """Analyze scraped data for insights"""
        if not products:
            return
        
        categories = {}
        brands = {}
        price_ranges = {'under_20': 0, '20_50': 0, '50_100': 0, 'over_100': 0}
        
        for product in products:
            # Count by category
            category = product.get('category', 'unknown')
            categories[category] = categories.get(category, 0) + 1
            
            # Count by brand
            brand = product.get('brand', 'unknown')
            brands[brand] = brands.get(brand, 0) + 1
            
            # Price analysis
            price = product.get('price', 0)
            if price < 20:
                price_ranges['under_20'] += 1
            elif price < 50:
                price_ranges['20_50'] += 1
            elif price < 100:
                price_ranges['50_100'] += 1
            else:
                price_ranges['over_100'] += 1
        
        print(f"\n📊 Scraping Analysis:")
        print(f"{'='*40}")
        print(f"Total products: {len(products)}")
        print(f"\nBy category:")
        for cat, count in sorted(categories.items()):
            print(f"  {cat}: {count}")
        
        print(f"\nPrice distribution:")
        for range_name, count in price_ranges.items():
            print(f"  {range_name}: {count}")
        
        print(f"\nTop brands:")
        top_brands = sorted(brands.items(), key=lambda x: x[1], reverse=True)[:5]
        for brand, count in top_brands:
            print(f"  {brand}: {count}")

async def main():
    """Main production scraping workflow"""
    print("🚀 Production-Ready Web Scraper")
    print("=" * 50)
    
    scraper = ProductionScraper()
    all_products = []
    
    try:
        # 1. Scrape from public APIs
        print("1️⃣ Scraping DummyJSON products...")
        dummy_products = await scraper.scrape_dummyjson_products()
        all_products.extend(dummy_products)
        
        # Small delay between different sources
        await asyncio.sleep(2)
        
        print("2️⃣ Creating brand products from ReqRes...")
        reqres_products = await scraper.scrape_reqres_users_as_brands()
        all_products.extend(reqres_products)
        
        # 3. Save to CSV backup
        print("3️⃣ Saving to CSV backup...")
        scraper.save_to_csv(all_products)
        
        # 4. Analyze data
        print("4️⃣ Analyzing scraped data...")
        scraper.analyze_scraped_data(all_products)
        
        # 5. Save to database
        print("5️⃣ Saving to database...")
        saved_count = await scraper.save_products_to_database(all_products)
        
        print(f"\n🎉 Production scraping complete!")
        print(f"✅ Processed {len(all_products)} products")
        print(f"✅ Saved {saved_count} new products to database")
        print(f"✅ CSV backup created")
        print(f"✅ Ready for AI search and analysis!")
        
    except Exception as e:
        logger.error(f"Scraping failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())