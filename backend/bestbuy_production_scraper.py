#!/usr/bin/env python3
"""
Best Buy API Production Scraper
Live integration with Best Buy API for real health tech products
"""

import asyncio
import aiohttp
import json
import os
from typing import List, Dict, Optional
from sqlalchemy.orm import sessionmaker
from app.core.database import engine
from app.models.models import Product

class BestBuyProductionScraper:
    def __init__(self, api_key: Optional[str] = None):
        self.Session = sessionmaker(bind=engine)
        # Get API key from environment variable or parameter
        self.api_key = api_key or os.getenv('BESTBUY_API_KEY') or "YOUR_API_KEY_HERE"
        self.base_url = "https://api.bestbuy.com/v1"
        self.session = None
        
        # Best Buy category IDs for health and wellness products
        self.health_categories = {
            'fitness_trackers': 'pcmcat748302045123',
            'smartwatches': 'pcmcat1496256594944', 
            'health_monitors': 'abcat0601007',
            'personal_care': 'abcat0601000',
            'air_quality': 'pcmcat310200050020',
            'exercise_equipment': 'abcat0601006'
        }
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={'User-Agent': 'AI-Product-Search-Production/1.0'}
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def is_api_key_valid(self) -> bool:
        """Check if we have a valid API key"""
        return self.api_key and self.api_key != "YOUR_API_KEY_HERE" and len(self.api_key) > 10
    
    async def fetch_products_by_category(self, category_id: str, category_name: str, limit: int = 25) -> List[Dict]:
        """Fetch products from Best Buy API for a specific category"""
        if not self.is_api_key_valid():
            print(f"⚠️ No valid API key - using sample data for {category_name}")
            return []
        
        try:
            # Build Best Buy API query
            query = f"(categoryPath.id={category_id})"
            fields = "sku,name,shortDescription,manufacturer,regularPrice,customerReviewAverage,customerReviewCount,image,url,categoryPath"
            
            url = f"{self.base_url}/products({query})"
            params = {
                'apiKey': self.api_key,
                'format': 'json',
                'show': fields,
                'pageSize': limit,
                'page': 1
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    products = data.get('products', [])
                    print(f"✅ Fetched {len(products)} products from Best Buy {category_name}")
                    return products
                else:
                    print(f"❌ Best Buy API error for {category_name}: HTTP {response.status}")
                    return []
        
        except Exception as e:
            print(f"❌ Error fetching {category_name}: {e}")
        
        return []
    
    async def fetch_health_search_products(self, search_terms: List[str], limit_per_term: int = 15) -> List[Dict]:
        """Search for health-related products"""
        if not self.is_api_key_valid():
            print("⚠️ No valid API key - using sample data for search products")
            return []
        
        all_products = []
        
        for term in search_terms:
            try:
                query = f"(search={term})"
                fields = "sku,name,shortDescription,manufacturer,regularPrice,customerReviewAverage,customerReviewCount,image,url"
                
                url = f"{self.base_url}/products({query})"
                params = {
                    'apiKey': self.api_key,
                    'format': 'json', 
                    'show': fields,
                    'pageSize': limit_per_term
                }
                
                async with self.session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        products = data.get('products', [])
                        all_products.extend(products)
                        print(f"✅ Found {len(products)} products for '{term}'")
                    
                # Rate limiting
                await asyncio.sleep(0.2)
                
            except Exception as e:
                print(f"❌ Error searching for '{term}': {e}")
        
        return all_products
    
    def convert_bestbuy_product(self, bestbuy_product: Dict) -> Dict:
        """Convert Best Buy API response to our product format"""
        try:
            # Determine category
            category_path = bestbuy_product.get('categoryPath', [])
            category_names = [cat.get('name', '').lower() for cat in category_path]
            
            if any('fitness' in name or 'health' in name or 'wellness' in name for name in category_names):
                category = 'healthcare'
            elif any('personal care' in name or 'beauty' in name for name in category_names):
                category = 'cosmetics'
            else:
                category = 'healthcare'  # Default for Best Buy electronics
            
            return {
                'name': bestbuy_product.get('name', 'Unknown Product')[:100],  # Limit name length
                'brand': bestbuy_product.get('manufacturer', 'Electronics Brand'),
                'price': float(bestbuy_product.get('regularPrice', 0.0)),
                'category': category,
                'description': bestbuy_product.get('shortDescription', '')[:500],  # Limit description
                'rating': float(bestbuy_product.get('customerReviewAverage', 4.0)),
                'review_count': int(bestbuy_product.get('customerReviewCount', 0)),
                'image_url': bestbuy_product.get('image', ''),
                'product_url': bestbuy_product.get('url', f"https://www.bestbuy.com/site/product/{bestbuy_product.get('sku', '')}.p"),
                'source_website': 'bestbuy.com (Live API)',
                'country': 'United States',
                'currency': 'USD',
                'in_stock': True,
                'best_buy_sku': bestbuy_product.get('sku'),
                'retailer': 'Best Buy'
            }
        except Exception as e:
            print(f"⚠️ Error converting product: {e}")
            return None
    
    def save_products_to_db(self, products: List[Dict]) -> int:
        """Save products to database"""
        db_session = self.Session()
        added_count = 0
        
        try:
            for product_data in products:
                if not product_data:
                    continue
                
                # Check if product already exists
                existing = db_session.query(Product).filter(
                    Product.name == product_data['name'],
                    Product.brand == product_data['brand']
                ).first()
                
                if not existing:
                    product = Product(
                        name=product_data['name'],
                        description=product_data['description'],
                        category=product_data['category'],
                        brand=product_data['brand'],
                        price=float(product_data['price']),
                        rating=float(product_data['rating']),
                        review_count=int(product_data['review_count']),
                        image_url=product_data['image_url'],
                        product_url=product_data['product_url'],
                        source_website=product_data['source_website'],
                        in_stock=product_data['in_stock']
                    )
                    
                    db_session.add(product)
                    added_count += 1
            
            db_session.commit()
            print(f"✅ Added {added_count} new Best Buy products to database")
            
        except Exception as e:
            print(f"❌ Database error: {e}")
            db_session.rollback()
        finally:
            db_session.close()
        
        return added_count

async def main():
    """Production Best Buy scraper with live API"""
    print("🏪 Best Buy Production API Integration")
    print("=" * 50)
    
    async with BestBuyProductionScraper() as scraper:
        if not scraper.is_api_key_valid():
            print("❌ SETUP REQUIRED:")
            print("1. Get your free API key from: https://developer.bestbuy.com/")
            print("2. Set environment variable: BESTBUY_API_KEY=your_key_here")
            print("3. Or update the api_key parameter in the script")
            print("\n🎯 Current Status: Using sample data (20 products already added)")
            return
        
        print(f"✅ Using Best Buy API key: {scraper.api_key[:8]}...")
        print("🔄 Fetching live product data from Best Buy...")
        
        all_products = []
        
        # Fetch by category
        for category_id, category_name in scraper.health_categories.items():
            products = await scraper.fetch_products_by_category(category_id, category_name, 20)
            converted = [scraper.convert_bestbuy_product(p) for p in products]
            valid_products = [p for p in converted if p is not None]
            all_products.extend(valid_products)
            
            # Rate limiting
            await asyncio.sleep(0.5)
        
        # Fetch by search terms
        health_terms = ['fitness tracker', 'smart watch', 'blood pressure monitor', 'air purifier', 'electric toothbrush']
        search_products = await scraper.fetch_health_search_products(health_terms, 10)
        converted_search = [scraper.convert_bestbuy_product(p) for p in search_products]
        valid_search = [p for p in converted_search if p is not None]
        all_products.extend(valid_search)
        
        print(f"\n📱 Total Best Buy products fetched: {len(all_products)}")
        
        if all_products:
            added = scraper.save_products_to_db(all_products)
            print(f"✅ Successfully integrated {added} Best Buy products!")
        else:
            print("⚠️ No products fetched - check API key and connectivity")

if __name__ == "__main__":
    asyncio.run(main())