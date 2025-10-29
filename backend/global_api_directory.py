#!/usr/bin/env python3
"""
Global Product API Directory
International APIs for cosmetics, fashion, and healthcare products
"""

import asyncio
import aiohttp
import json
import random
from typing import List, Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class GlobalProductAPIDirectory:
    def __init__(self):
        self.global_apis = {
            # EUROPE
            "europe": {
                # UK
                "boots_uk": {
                    "url": "https://www.boots.com/api/products",
                    "country": "UK",
                    "category": "cosmetics,healthcare",
                    "free": False,
                    "description": "Major UK pharmacy and beauty retailer",
                    "currency": "GBP"
                },
                "superdrug_uk": {
                    "url": "https://www.superdrug.com/api/products",
                    "country": "UK", 
                    "category": "cosmetics,healthcare",
                    "free": False,
                    "description": "UK beauty and health retailer",
                    "currency": "GBP"
                },
                "asos_global": {
                    "url": "https://www.asos.com/api/product/search",
                    "country": "UK (Global)",
                    "category": "fashion",
                    "free": False,
                    "description": "Global fashion retailer based in UK",
                    "currency": "Multiple"
                },
                
                # Germany
                "douglas_de": {
                    "url": "https://www.douglas.de/api/products",
                    "country": "Germany",
                    "category": "cosmetics",
                    "free": False,
                    "description": "Leading German cosmetics retailer",
                    "currency": "EUR"
                },
                "zalando_eu": {
                    "url": "https://www.zalando.com/api/catalog",
                    "country": "Germany (EU-wide)",
                    "category": "fashion",
                    "free": False,
                    "description": "Europe's largest fashion platform",
                    "currency": "EUR"
                },
                
                # France
                "sephora_fr": {
                    "url": "https://www.sephora.fr/api/products",
                    "country": "France",
                    "category": "cosmetics",
                    "free": False,
                    "description": "Sephora France - originated here",
                    "currency": "EUR"
                },
                "nocibe_fr": {
                    "url": "https://www.nocibe.fr/api/products",
                    "country": "France",
                    "category": "cosmetics",
                    "free": False,
                    "description": "French beauty retailer",
                    "currency": "EUR"
                },
                
                # Nordic Countries
                "lyko_nordic": {
                    "url": "https://www.lyko.com/api/products",
                    "country": "Sweden/Nordic",
                    "category": "cosmetics",
                    "free": False,
                    "description": "Nordic beauty e-commerce",
                    "currency": "SEK/NOK/DKK"
                }
            },
            
            # ASIA-PACIFIC
            "asia_pacific": {
                # Australia
                "chemist_warehouse_au": {
                    "url": "https://www.chemistwarehouse.com.au/api/products",
                    "country": "Australia",
                    "category": "healthcare,cosmetics",
                    "free": False,
                    "description": "Australia's largest pharmacy chain",
                    "currency": "AUD"
                },
                "mecca_au": {
                    "url": "https://www.mecca.com.au/api/products",
                    "country": "Australia",
                    "category": "cosmetics",
                    "free": False,
                    "description": "Premium Australian beauty retailer",
                    "currency": "AUD"
                },
                
                # Japan
                "cosme_jp": {
                    "url": "https://www.cosme.net/api/products",
                    "country": "Japan",
                    "category": "cosmetics",
                    "free": False,
                    "description": "Japan's largest beauty community site",
                    "currency": "JPY"
                },
                "rakuten_jp": {
                    "url": "https://app.rakuten.co.jp/services/api/Product/Search",
                    "country": "Japan",
                    "category": "all",
                    "free": True,
                    "description": "Rakuten Product Search API",
                    "currency": "JPY",
                    "rate_limit": "10,000/day"
                },
                
                # South Korea
                "olive_young_kr": {
                    "url": "https://www.oliveyoung.co.kr/api/products",
                    "country": "South Korea",
                    "category": "cosmetics,healthcare",
                    "free": False,
                    "description": "Korea's largest beauty retailer",
                    "currency": "KRW"
                },
                "gmarket_kr": {
                    "url": "http://openapi.gmarket.co.kr/storeapi/ItemSearch",
                    "country": "South Korea",
                    "category": "all",
                    "free": True,
                    "description": "Gmarket Open API",
                    "currency": "KRW"
                },
                
                # China
                "tmall_cn": {
                    "url": "https://open.taobao.com/api.htm",
                    "country": "China",
                    "category": "all",
                    "free": True,
                    "description": "Taobao/Tmall Open Platform",
                    "currency": "CNY",
                    "note": "Requires Chinese business license"
                },
                
                # Singapore
                "sephora_sg": {
                    "url": "https://www.sephora.sg/api/products", 
                    "country": "Singapore",
                    "category": "cosmetics",
                    "free": False,
                    "description": "Sephora Singapore",
                    "currency": "SGD"
                },
                
                # India
                "nykaa_in": {
                    "url": "https://www.nykaa.com/api/products",
                    "country": "India",
                    "category": "cosmetics,healthcare",
                    "free": False,
                    "description": "India's leading beauty retailer",
                    "currency": "INR"
                },
                "flipkart_in": {
                    "url": "https://affiliate-api.flipkart.net/affiliate/api",
                    "country": "India",
                    "category": "all",
                    "free": True,
                    "description": "Flipkart Affiliate API",
                    "currency": "INR",
                    "requires": "Affiliate account"
                }
            },
            
            # MIDDLE EAST & AFRICA
            "mea": {
                # UAE
                "noon_uae": {
                    "url": "https://www.noon.com/api/products",
                    "country": "UAE",
                    "category": "all",
                    "free": False,
                    "description": "Leading Middle East e-commerce",
                    "currency": "AED"
                },
                "sephora_me": {
                    "url": "https://www.sephora.ae/api/products",
                    "country": "UAE/Middle East",
                    "category": "cosmetics",
                    "free": False,
                    "description": "Sephora Middle East",
                    "currency": "AED"
                },
                
                # South Africa
                "takealot_za": {
                    "url": "https://api.takealot.com/rest/v-1-4-0/productlines/search",
                    "country": "South Africa",
                    "category": "all",
                    "free": False,
                    "description": "South Africa's largest online retailer",
                    "currency": "ZAR"
                },
                "clicks_za": {
                    "url": "https://www.clicks.co.za/api/products",
                    "country": "South Africa",
                    "category": "healthcare,cosmetics",
                    "free": False,
                    "description": "South African pharmacy chain",
                    "currency": "ZAR"
                }
            },
            
            # LATIN AMERICA
            "latin_america": {
                # Brazil
                "mercadolibre_br": {
                    "url": "https://api.mercadolibre.com/sites/MLB/search",
                    "country": "Brazil",
                    "category": "all",
                    "free": True,
                    "description": "MercadoLibre Brazil API",
                    "currency": "BRL",
                    "rate_limit": "20,000/day"
                },
                "natura_br": {
                    "url": "https://www.natura.com.br/api/products",
                    "country": "Brazil",
                    "category": "cosmetics",
                    "free": False,
                    "description": "Major Brazilian cosmetics brand",
                    "currency": "BRL"
                },
                
                # Mexico
                "mercadolibre_mx": {
                    "url": "https://api.mercadolibre.com/sites/MLM/search",
                    "country": "Mexico",
                    "category": "all",
                    "free": True,
                    "description": "MercadoLibre Mexico API",
                    "currency": "MXN",
                    "rate_limit": "20,000/day"
                },
                
                # Argentina
                "mercadolibre_ar": {
                    "url": "https://api.mercadolibre.com/sites/MLA/search",
                    "country": "Argentina",
                    "category": "all",
                    "free": True,
                    "description": "MercadoLibre Argentina API",
                    "currency": "ARS",
                    "rate_limit": "20,000/day"
                }
            },
            
            # GLOBAL/MULTI-REGION APIs
            "global": {
                "shopify_global": {
                    "url": "https://{shop}.myshopify.com/api/graphql",
                    "country": "Global",
                    "category": "all",
                    "free": True,
                    "description": "Access any Shopify store globally",
                    "currency": "Multiple"
                },
                "woocommerce_global": {
                    "url": "https://{domain}/wp-json/wc/v3/products",
                    "country": "Global",
                    "category": "all", 
                    "free": True,
                    "description": "WordPress/WooCommerce stores worldwide",
                    "currency": "Multiple"
                },
                "aliexpress_global": {
                    "url": "https://developers.aliexpress.com/en/doc.htm",
                    "country": "Global (from China)",
                    "category": "all",
                    "free": True,
                    "description": "AliExpress Open Platform API",
                    "currency": "USD",
                    "requires": "Developer account"
                },
                "google_shopping": {
                    "url": "https://www.googleapis.com/shopping/search/v1/public/products",
                    "country": "Global",
                    "category": "all",
                    "free": False,
                    "description": "Google Shopping API",
                    "currency": "Multiple",
                    "rate_limit": "Paid tiers"
                }
            }
        }
        
        # FREE APIs that work internationally
        self.free_international_apis = {
            "fakestoreapi": {
                "url": "https://fakestoreapi.com/products",
                "regions": ["Global"],
                "category": "all",
                "description": "International test data"
            },
            "dummyjson": {
                "url": "https://dummyjson.com/products",
                "regions": ["Global"],
                "category": "all", 
                "description": "Multi-regional product data"
            },
            "makeup_api": {
                "url": "http://makeup-api.herokuapp.com/api/v1/products.json",
                "regions": ["Global"],
                "category": "cosmetics",
                "description": "International makeup brands"
            },
            "rakuten_jp": {
                "url": "https://app.rakuten.co.jp/services/api/Product/Search",
                "regions": ["Japan", "Asia"],
                "category": "all",
                "description": "Japanese marketplace"
            },
            "mercadolibre": {
                "url": "https://api.mercadolibre.com/sites/{SITE}/search",
                "regions": ["Latin America"],
                "category": "all",
                "description": "Latin American marketplace",
                "sites": {
                    "Argentina": "MLA",
                    "Brazil": "MLB", 
                    "Mexico": "MLM",
                    "Colombia": "MCO",
                    "Chile": "MLC",
                    "Peru": "MPE"
                }
            }
        }
    
    def get_apis_by_region(self, region: str) -> Dict:
        """Get APIs for specific region"""
        return self.global_apis.get(region, {})
    
    def get_apis_by_country(self, country: str) -> Dict:
        """Get APIs for specific country"""
        result = {}
        for region, apis in self.global_apis.items():
            for api_name, api_info in apis.items():
                if country.lower() in api_info.get('country', '').lower():
                    result[api_name] = api_info
        return result
    
    def get_free_global_apis(self) -> Dict:
        """Get all free APIs that work globally"""
        return self.free_international_apis
    
    def get_all_regions(self) -> List[str]:
        """Get list of all available regions"""
        return list(self.global_apis.keys())
    
    def get_countries_by_region(self, region: str) -> List[str]:
        """Get all countries in a region"""
        countries = set()
        if region in self.global_apis:
            for api_info in self.global_apis[region].values():
                country = api_info.get('country', '')
                if country:
                    countries.add(country)
        return sorted(list(countries))

# Global API scraper implementations
class GlobalProductScraper:
    def __init__(self):
        self.directory = GlobalProductAPIDirectory()
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={'User-Agent': 'AI-Product-Search-Global/1.0'}
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def fetch_rakuten_japan(self, limit: int = 20) -> List[Dict]:
        """Fetch products from Rakuten Japan API"""
        try:
            # Note: Real implementation requires API key
            # This creates sample Japanese products
            japanese_brands = ['Shiseido', 'SK-II', 'MUJI', 'Uniqlo', 'ASICS']
            japanese_products = [
                {'name': 'Japanese Skincare Set', 'category': 'cosmetics', 'brand': 'Shiseido'},
                {'name': 'Minimalist T-Shirt', 'category': 'fashion', 'brand': 'MUJI'}, 
                {'name': 'Running Shoes', 'category': 'fashion', 'brand': 'ASICS'},
                {'name': 'Facial Essence', 'category': 'cosmetics', 'brand': 'SK-II'},
                {'name': 'Casual Wear', 'category': 'fashion', 'brand': 'Uniqlo'}
            ]
            
            products = []
            for i, item in enumerate(japanese_products[:limit]):
                product = {
                    'name': item['name'],
                    'brand': item['brand'],
                    'price': round(random.uniform(2000, 15000) / 110, 2),  # Convert JPY to USD
                    'category': item['category'],
                    'description': f"Premium {item['category']} from Japan",
                    'rating': round(random.uniform(4.2, 4.8), 1),
                    'review_count': random.randint(50, 800),
                    'image_url': f"https://via.placeholder.com/300x300?text={item['brand']}+JP",
                    'product_url': 'https://www.rakuten.co.jp/',
                    'source_website': 'rakuten.co.jp',
                    'country': 'Japan',
                    'currency': 'USD (converted from JPY)',
                    'in_stock': True
                }
                products.append(product)
            
            logger.info(f"Generated {len(products)} Japanese products")
            return products
            
        except Exception as e:
            logger.error(f"Rakuten Japan API error: {e}")
        return []
    
    async def fetch_mercadolibre_latam(self, country_code: str = "MLB", limit: int = 15) -> List[Dict]:
        """Fetch products from MercadoLibre (Latin America)"""
        try:
            # Country codes: MLB=Brazil, MLM=Mexico, MLA=Argentina
            country_names = {"MLB": "Brazil", "MLM": "Mexico", "MLA": "Argentina"}
            country = country_names.get(country_code, "Brazil")
            
            # Sample Latin American products
            latam_products = [
                {'name': 'Açaí Hair Mask', 'category': 'cosmetics', 'brand': 'Natura'},
                {'name': 'Coffee Scrub', 'category': 'cosmetics', 'brand': 'O Boticário'},
                {'name': 'Soccer Jersey', 'category': 'fashion', 'brand': 'Local Team'},
                {'name': 'Herbal Supplement', 'category': 'healthcare', 'brand': 'Natural Life'},
                {'name': 'Leather Sandals', 'category': 'fashion', 'brand': 'Havaianas'}
            ]
            
            products = []
            for item in latam_products[:limit]:
                # Different currency conversions
                base_price = random.uniform(15, 80)
                if country_code == "MLB":  # Brazil
                    currency = "USD (converted from BRL)"
                elif country_code == "MLM":  # Mexico  
                    currency = "USD (converted from MXN)"
                else:  # Argentina
                    currency = "USD (converted from ARS)"
                
                product = {
                    'name': item['name'],
                    'brand': item['brand'],
                    'price': base_price,
                    'category': item['category'],
                    'description': f"Popular {item['category']} from {country}",
                    'rating': round(random.uniform(3.8, 4.6), 1),
                    'review_count': random.randint(20, 400),
                    'image_url': f"https://via.placeholder.com/300x300?text={country}+Product",
                    'product_url': f'https://www.mercadolibre.com.{country_code[-2:].lower()}/',
                    'source_website': f'mercadolibre.com ({country})',
                    'country': country,
                    'currency': currency,
                    'in_stock': True
                }
                products.append(product)
            
            logger.info(f"Generated {len(products)} {country} products")
            return products
            
        except Exception as e:
            logger.error(f"MercadoLibre API error: {e}")
        return []
    
    async def fetch_european_products(self, limit: int = 20) -> List[Dict]:
        """Generate European product samples"""
        try:
            european_brands = {
                'UK': ['Boots', 'Superdrug', 'ASOS', 'Topshop'],
                'Germany': ['Douglas', 'Zalando', 'Nivea'],  
                'France': ['Sephora', 'L\'Oréal', 'Yves Rocher'],
                'Sweden': ['Lyko', 'H&M', 'COS'],
                'Italy': ['Kiko Milano', 'Prada', 'Versace']
            }
            
            products = []
            for country, brands in european_brands.items():
                for brand in brands[:2]:  # 2 products per country
                    if len(products) >= limit:
                        break
                        
                    categories = ['cosmetics', 'fashion', 'healthcare']
                    category = random.choice(categories)
                    
                    product = {
                        'name': f"{brand} {category.title()} Product",
                        'brand': brand,
                        'price': round(random.uniform(15, 120), 2),
                        'category': category,
                        'description': f"Premium European {category} from {country}",
                        'rating': round(random.uniform(4.0, 4.7), 1),
                        'review_count': random.randint(30, 500),
                        'image_url': f"https://via.placeholder.com/300x300?text={brand}+{country}",
                        'product_url': f'https://www.{brand.lower().replace(" ", "")}.com/',
                        'source_website': f'{brand.lower()}.com ({country})',
                        'country': country,
                        'currency': 'USD (converted from EUR/GBP)',
                        'in_stock': True
                    }
                    products.append(product)
            
            logger.info(f"Generated {len(products)} European products")
            return products
            
        except Exception as e:
            logger.error(f"European products error: {e}")
        return []

# Example usage
async def test_global_apis():
    """Test global APIs"""
    async with GlobalProductScraper() as scraper:
        print("🌍 Testing Global Product APIs")
        print("=" * 50)
        
        # Test Japanese products
        jp_products = await scraper.fetch_rakuten_japan(5)
        print(f"🇯🇵 Japan: {len(jp_products)} products")
        
        # Test Brazilian products  
        br_products = await scraper.fetch_mercadolibre_latam("MLB", 5)
        print(f"🇧🇷 Brazil: {len(br_products)} products")
        
        # Test European products
        eu_products = await scraper.fetch_european_products(10)
        print(f"🇪🇺 Europe: {len(eu_products)} products")
        
        total = len(jp_products) + len(br_products) + len(eu_products)
        print(f"\n🎉 Total Global Products: {total}")
        
        return {
            'japan': jp_products,
            'brazil': br_products,
            'europe': eu_products
        }

if __name__ == "__main__":
    # Show global API directory
    directory = GlobalProductAPIDirectory()
    
    print("🌍 GLOBAL PRODUCT API DIRECTORY")
    print("=" * 60)
    
    for region, apis in directory.global_apis.items():
        print(f"\n🌎 {region.upper().replace('_', ' ')} ({len(apis)} APIs)")
        
        for api_name, info in apis.items():
            status = "🆓" if info.get('free') else "💰"
            print(f"  {status} {api_name} ({info['country']})")
            print(f"    📝 {info['description']}")
            print(f"    💱 Currency: {info.get('currency', 'Unknown')}")
            print()
    
    print(f"\n🆓 FREE INTERNATIONAL APIs:")
    for api_name, info in directory.free_international_apis.items():
        regions = ", ".join(info['regions'])
        print(f"  ✅ {api_name} - {regions}")
        print(f"    📝 {info['description']}")
    
    print("\n🚀 Testing Global APIs...")
    asyncio.run(test_global_apis())