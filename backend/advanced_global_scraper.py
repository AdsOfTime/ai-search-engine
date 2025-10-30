#!/usr/bin/env python3
"""
Advanced Global Product Scraper
Fetch products from free international APIs to expand the catalog
"""

import asyncio
import aiohttp
import json
import random
from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from app.core.database import engine
from app.models.models import Product
from global_api_directory import GlobalProductScraper

class AdvancedGlobalScraper:
    def __init__(self):
        self.Session = sessionmaker(bind=engine)
        self.global_scraper = None
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={'User-Agent': 'AI-Product-Search-Global/1.0'}
        )
        self.global_scraper = GlobalProductScraper()
        await self.global_scraper.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
        if self.global_scraper:
            await self.global_scraper.__aexit__(exc_type, exc_val, exc_tb)
    
    async def fetch_dummyjson_products(self) -> List[Dict]:
        """Fetch from DummyJSON - free international product API"""
        try:
            async with self.session.get('https://dummyjson.com/products?limit=30') as response:
                if response.status == 200:
                    data = await response.json()
                    products = []
                    
                    for item in data.get('products', []):
                        # Map to our categories
                        category_mapping = {
                            'beauty': 'cosmetics',
                            'fragrances': 'cosmetics',
                            'skincare': 'cosmetics',
                            'mens-shirts': 'fashion',
                            'womens-dresses': 'fashion',
                            'womens-shoes': 'fashion',
                            'mens-shoes': 'fashion',
                            'womens-watches': 'fashion',
                            'mens-watches': 'fashion',
                            'sunglasses': 'fashion',
                            'automotive': 'healthcare',  # Map to healthcare for demo
                            'motorcycle': 'fashion',
                            'lighting': 'healthcare'
                        }
                        
                        category = category_mapping.get(item.get('category'), 'fashion')
                        
                        product = {
                            'name': item['title'],
                            'brand': item.get('brand', 'International Brand'),
                            'price': float(item['price']),
                            'category': category,
                            'description': item.get('description', ''),
                            'rating': float(item.get('rating', 4.0)),
                            'review_count': random.randint(10, 150),
                            'image_url': item.get('thumbnail', ''),
                            'product_url': 'https://dummyjson.com/products/' + str(item['id']),
                            'source_website': 'dummyjson.com (Global)',
                            'country': 'International',
                            'currency': 'USD',
                            'in_stock': True
                        }
                        products.append(product)
                    
                    print(f"✅ Fetched {len(products)} products from DummyJSON")
                    return products
        except Exception as e:
            print(f"❌ DummyJSON API error: {e}")
        return []
    
    async def fetch_platzi_fake_store(self) -> List[Dict]:
        """Fetch from Platzi Fake Store API - another free API"""
        try:
            async with self.session.get('https://api.escuelajs.co/api/v1/products?limit=25') as response:
                if response.status == 200:
                    data = await response.json()
                    products = []
                    
                    for item in data:
                        # Map categories
                        category_name = item.get('category', {}).get('name', '').lower()
                        if 'clothes' in category_name or 'fashion' in category_name:
                            category = 'fashion'
                        elif 'electronics' in category_name:
                            category = 'healthcare'  # Map electronics to healthcare
                        else:
                            category = 'cosmetics'
                        
                        product = {
                            'name': item['title'],
                            'brand': 'Global Brand',
                            'price': float(item['price']),
                            'category': category,
                            'description': item.get('description', '')[:500],  # Limit description
                            'rating': round(random.uniform(3.8, 4.7), 1),
                            'review_count': random.randint(5, 120),
                            'image_url': item.get('images', [''])[0] if item.get('images') else '',
                            'product_url': f"https://platzi.com/products/{item['id']}",
                            'source_website': 'platzi.com (Global)',
                            'country': 'International',
                            'currency': 'USD',
                            'in_stock': True
                        }
                        products.append(product)
                    
                    print(f"✅ Fetched {len(products)} products from Platzi API")
                    return products
        except Exception as e:
            print(f"❌ Platzi API error: {e}")
        return []
    
    async def generate_regional_products(self) -> List[Dict]:
        """Generate products from different global regions"""
        regional_data = {
            'Asia-Pacific': {
                'countries': ['Japan', 'South Korea', 'Australia', 'Singapore', 'India'],
                'brands': ['Shiseido', 'SK-II', 'MUJI', 'Innisfree', 'Nykaa'],
                'products': ['K-Beauty Serum', 'Japanese Sunscreen', 'Ayurvedic Cream', 'Pearl Face Mask', 'Bamboo Cleanser']
            },
            'Europe': {
                'countries': ['France', 'Germany', 'UK', 'Sweden', 'Italy'], 
                'brands': ['L\'Oréal', 'Nivea', 'Boots', 'Lyko', 'Kiko Milano'],
                'products': ['French Perfume', 'German Skincare', 'British Tea Tree Oil', 'Nordic Moisturizer', 'Italian Foundation']
            },
            'Latin America': {
                'countries': ['Brazil', 'Mexico', 'Argentina', 'Colombia', 'Chile'],
                'brands': ['Natura', 'O Boticário', 'Yanbal', 'Ésika', 'Avon Latam'],
                'products': ['Açaí Hair Mask', 'Cactus Face Cream', 'Coffee Body Scrub', 'Aloe Vera Gel', 'Quinoa Shampoo']
            },
            'Middle East & Africa': {
                'countries': ['UAE', 'South Africa', 'Egypt', 'Morocco', 'Nigeria'],
                'brands': ['Arabian Oud', 'Clicks', 'Nefertiti', 'Atlas Beauty', 'Zaron'],
                'products': ['Argan Oil Treatment', 'Black Soap Cleanser', 'Rose Water Toner', 'Shea Butter Cream', 'Oud Perfume']
            }
        }
        
        products = []
        for region, data in regional_data.items():
            for i in range(5):  # 5 products per region
                country = random.choice(data['countries'])
                brand = random.choice(data['brands'])
                product_name = random.choice(data['products'])
                
                product = {
                    'name': f"{brand} {product_name}",
                    'brand': brand,
                    'price': round(random.uniform(12, 85), 2),
                    'category': random.choice(['cosmetics', 'fashion', 'healthcare']),
                    'description': f"Premium {product_name.lower()} from {country}, popular in {region}",
                    'rating': round(random.uniform(4.1, 4.8), 1),
                    'review_count': random.randint(25, 300),
                    'image_url': f"https://via.placeholder.com/300x300?text={brand.replace(' ', '+')}",
                    'product_url': f"https://www.{brand.lower().replace(' ', '').replace('\'', '')}.com/",
                    'source_website': f'{brand.lower().replace(" ", "")}.com ({country})',
                    'country': country,
                    'region': region,
                    'currency': 'USD (converted)',
                    'in_stock': True
                }
                products.append(product)
        
        print(f"✅ Generated {len(products)} regional products")
        return products
    
    def save_products_to_db(self, products: List[Dict]):
        """Save products to database"""
        db_session = self.Session()
        added_count = 0
        
        try:
            for product_data in products:
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
            print(f"✅ Added {added_count} new products to database")
            
        except Exception as e:
            print(f"❌ Database error: {e}")
            db_session.rollback()
        finally:
            db_session.close()
        
        return added_count

async def main():
    """Main function to scrape global products"""
    print("🌍 AI Product Search Engine - Global Product Scraper")
    print("=" * 65)
    
    async with AdvancedGlobalScraper() as scraper:
        all_products = []
        
        print("🌐 Fetching from DummyJSON API...")
        dummyjson_products = await scraper.fetch_dummyjson_products()
        all_products.extend(dummyjson_products)
        
        print("\n🌐 Fetching from Platzi Fake Store API...")
        platzi_products = await scraper.fetch_platzi_fake_store()
        all_products.extend(platzi_products)
        
        print("\n🌍 Generating regional products...")
        regional_products = await scraper.generate_regional_products()
        all_products.extend(regional_products)
        
        print("\n🌏 Generating Asian products...")
        asian_products = await scraper.global_scraper.fetch_rakuten_japan(10)
        all_products.extend(asian_products)
        
        print("\n🌎 Generating Latin American products...")
        latam_products = await scraper.global_scraper.fetch_mercadolibre_latam("MLB", 8)
        all_products.extend(latam_products)
        
        print("\n🌍 Generating European products...")
        european_products = await scraper.global_scraper.fetch_european_products(12)
        all_products.extend(european_products)
        
        print(f"\n📦 Total products collected: {len(all_products)}")
        
        # Save to database
        print("\n💾 Saving products to database...")
        added = scraper.save_products_to_db(all_products)
        
        print(f"\n🎉 Global product scraping complete!")
        print(f"📊 Products added to database: {added}")
        print(f"🌍 Regions covered: Asia-Pacific, Europe, Latin America, Middle East & Africa")
        print(f"🏪 Sources: DummyJSON, Platzi API, Regional generators")

if __name__ == "__main__":
    asyncio.run(main())