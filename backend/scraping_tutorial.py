#!/usr/bin/env python3
"""
Web Scraping Tutorial - How to Scrape Real Websites
Shows different techniques for getting product data
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import random
from typing import List, Dict

class WebScrapingTutorial:
    """
    Tutorial showing different web scraping techniques
    """
    
    def __init__(self):
        # Important: Always use proper headers to avoid blocking
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    def scrape_method_1_requests_beautifulsoup(self):
        """
        Method 1: Using requests + BeautifulSoup (Most Common)
        Good for: Static content, simple pages
        """
        print("\n🔧 Method 1: Requests + BeautifulSoup")
        print("-" * 40)
        
        try:
            # Example: Scraping a simple product page
            url = "https://httpbin.org/html"  # Test URL that returns HTML
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()  # Raise exception for bad status codes
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract data (example selectors)
            title = soup.find('h1')
            print(f"✅ Page title: {title.text if title else 'Not found'}")
            
            # Simulate product extraction
            print("✅ This method works for static HTML content")
            print("💡 Use this for: Simple e-commerce sites, blogs, static pages")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def scrape_method_2_api_endpoints(self):
        """
        Method 2: Finding Hidden APIs (Best Method!)
        Good for: Modern sites, faster scraping
        """
        print("\n🔧 Method 2: Hidden API Discovery")
        print("-" * 40)
        
        try:
            # Many sites have hidden JSON APIs
            # Example: JSONPlaceholder (demo API)
            api_url = "https://jsonplaceholder.typicode.com/posts/1"
            
            response = requests.get(api_url, headers=self.headers)
            data = response.json()
            
            print(f"✅ API Response: {data.get('title', 'No title')}")
            print("💡 How to find APIs:")
            print("   1. Open browser dev tools (F12)")
            print("   2. Go to Network tab")
            print("   3. Browse the site, look for XHR/Fetch requests")
            print("   4. Find JSON responses with product data")
            print("   5. Use those URLs in your scraper!")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def scrape_method_3_sitemap_crawling(self):
        """
        Method 3: Using Sitemaps to Find Products
        Good for: Discovering all product URLs
        """
        print("\n🔧 Method 3: Sitemap Crawling")
        print("-" * 40)
        
        try:
            # Most sites have sitemaps at /sitemap.xml
            sitemap_url = "https://httpbin.org/xml"  # Example XML response
            
            response = requests.get(sitemap_url, headers=self.headers)
            
            print("✅ Sitemap method:")
            print("   1. Check /sitemap.xml or /robots.txt")
            print("   2. Parse XML to find product URLs")
            print("   3. Scrape each product page individually")
            print("💡 This method finds ALL products on a site")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def show_real_scraping_targets(self):
        """
        Show real websites you can scrape (legally)
        """
        print("\n🎯 Real Scraping Opportunities")
        print("-" * 40)
        
        targets = {
            "Easy Targets (Good for beginners)": [
                "🟢 books.toscrape.com - Practice scraping site",
                "🟢 httpbin.org - HTTP testing service", 
                "🟢 quotes.toscrape.com - Quotes with pagination",
                "🟢 scrapethissite.com - Scraping challenges"
            ],
            
            "Public APIs (Best option)": [
                "🔵 fakestoreapi.com - Sample products",
                "🔵 makeup-api.herokuapp.com - Real cosmetics",
                "🔵 dummyjson.com/products - Sample e-commerce data",
                "🔵 reqres.in - User/product API"
            ],
            
            "Real Sites (Check robots.txt first!)": [
                "🟡 ebay.com - Auction data (public listings)",
                "🟡 etsy.com - Handmade products (public listings)",
                "🟡 github.com - Open source projects",
                "🟡 reddit.com - Public posts (has API)"
            ],
            
            "Advanced Targets (Need Selenium)": [
                "🔴 React/Vue sites - Need to wait for JS",
                "🔴 Infinite scroll pages - Need automation", 
                "🔴 Login-required sites - Need authentication",
                "🔴 Anti-bot sites - Need proxy rotation"
            ]
        }
        
        for category, sites in targets.items():
            print(f"\n{category}:")
            for site in sites:
                print(f"  {site}")
    
    def show_legal_considerations(self):
        """
        Important legal and ethical guidelines
        """
        print("\n⚖️ Legal & Ethical Guidelines")
        print("-" * 40)
        
        guidelines = [
            "✅ Always check robots.txt first (/robots.txt)",
            "✅ Respect rate limits (1-2 seconds between requests)",
            "✅ Use proper User-Agent headers",
            "✅ Only scrape publicly available data",
            "✅ Don't overload servers with too many requests",
            "✅ Consider using official APIs when available",
            "❌ Don't scrape copyrighted content",
            "❌ Don't ignore Terms of Service",
            "❌ Don't scrape personal/private information",
            "❌ Don't use scraped data commercially without permission"
        ]
        
        for guideline in guidelines:
            print(f"  {guideline}")
    
    def create_scraper_template(self):
        """
        Create a template scraper you can customize
        """
        template = '''#!/usr/bin/env python3
"""
Custom Product Scraper Template
Customize this for your target website
"""

import requests
from bs4 import BeautifulSoup
import time
import random

class CustomProductScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.base_url = "https://example-shop.com"
        self.delay = (1, 3)  # Random delay between requests
    
    def scrape_product_page(self, product_url):
        """Scrape a single product page"""
        try:
            response = requests.get(product_url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Customize these selectors for your target site
            product_data = {
                'name': soup.select_one('.product-title').text.strip(),
                'price': soup.select_one('.price').text.strip(),
                'rating': soup.select_one('.rating').text.strip(),
                'description': soup.select_one('.description').text.strip(),
                'image_url': soup.select_one('.product-image img')['src'],
                'in_stock': 'in stock' in soup.text.lower()
            }
            
            return product_data
            
        except Exception as e:
            print(f"Error scraping {product_url}: {e}")
            return None
    
    def scrape_category(self, category_url, max_pages=5):
        """Scrape multiple pages of products"""
        products = []
        
        for page in range(1, max_pages + 1):
            try:
                page_url = f"{category_url}?page={page}"
                response = requests.get(page_url, headers=self.headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find product links on the page
                product_links = soup.select('.product-item a')
                
                for link in product_links:
                    product_url = link.get('href')
                    if product_url:
                        full_url = self.base_url + product_url
                        product = self.scrape_product_page(full_url)
                        if product:
                            products.append(product)
                        
                        # Be polite - don't overwhelm the server
                        time.sleep(random.uniform(*self.delay))
                
                print(f"Scraped page {page}, found {len(product_links)} products")
                
            except Exception as e:
                print(f"Error scraping page {page}: {e}")
                break
        
        return products

# Usage:
# scraper = CustomProductScraper()
# products = scraper.scrape_category("https://example-shop.com/cosmetics")
'''
        
        with open('C:\\AI Search\\backend\\scraper_template.py', 'w', encoding='utf-8') as f:
            f.write(template)
        
        print("✅ Created scraper_template.py - customize it for your target site!")

def main():
    """Run the web scraping tutorial"""
    print("🕷️ Web Scraping Tutorial for AI Product Search Engine")
    print("=" * 60)
    
    tutorial = WebScrapingTutorial()
    
    # Show different scraping methods
    tutorial.scrape_method_1_requests_beautifulsoup()
    tutorial.scrape_method_2_api_endpoints() 
    tutorial.scrape_method_3_sitemap_crawling()
    
    # Show scraping targets
    tutorial.show_real_scraping_targets()
    
    # Legal guidelines
    tutorial.show_legal_considerations()
    
    # Create template
    print("\n📝 Creating Custom Scraper Template...")
    tutorial.create_scraper_template()
    
    print(f"\n🎓 Tutorial Complete!")
    print("Next steps:")
    print("1. Choose a target website from the list above")
    print("2. Check their robots.txt and terms of service")
    print("3. Customize scraper_template.py for that site")
    print("4. Start with small tests (10-20 products)")
    print("5. Scale up gradually with proper rate limiting")

if __name__ == "__main__":
    main()