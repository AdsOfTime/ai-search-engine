#!/usr/bin/env python3
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
