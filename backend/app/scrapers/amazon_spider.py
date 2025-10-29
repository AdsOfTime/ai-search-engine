import scrapy
from typing import Dict, Any

class AmazonProductSpider(scrapy.Spider):
    name = "amazon_products"
    allowed_domains = ["amazon.com"]
    
    def __init__(self, category="cosmetics", *args, **kwargs):
        super(AmazonProductSpider, self).__init__(*args, **kwargs)
        self.category = category
        
        # Search URLs for different categories
        search_urls = {
            "cosmetics": "https://www.amazon.com/s?k=cosmetics&ref=sr_pg_1",
            "fashion": "https://www.amazon.com/s?k=fashion&ref=sr_pg_1", 
            "healthcare": "https://www.amazon.com/s?k=health+supplements&ref=sr_pg_1"
        }
        
        self.start_urls = [search_urls.get(category, search_urls["cosmetics"])]
    
    def parse(self, response):
        """Parse search results page"""
        # Extract product URLs from search results
        product_urls = response.css('[data-component-type="s-search-result"] h2 a::attr(href)').getall()
        
        for url in product_urls[:20]:  # Limit for demo
            if url:
                full_url = response.urljoin(url)
                yield response.follow(full_url, self.parse_product)
    
    def parse_product(self, response):
        """Parse individual product page"""
        yield {
            'name': response.css('#productTitle::text').get().strip() if response.css('#productTitle::text').get() else '',
            'price': self.extract_price(response),
            'rating': self.extract_rating(response),
            'review_count': self.extract_review_count(response),
            'description': self.extract_description(response),
            'image_url': response.css('#landingImage::attr(src)').get(),
            'product_url': response.url,
            'category': self.category,
            'source_website': 'amazon.com',
            'brand': response.css('#bylineInfo::text').re_first(r'Brand: (.+)') or '',
            'in_stock': 'Available' in response.text or 'Add to Cart' in response.text
        }
    
    def extract_price(self, response):
        """Extract price from product page"""
        # Try multiple price selectors
        price_selectors = [
            '.a-price-whole::text',
            '.a-offscreen::text',
            '#price_inside_buybox::text'
        ]
        
        for selector in price_selectors:
            price_text = response.css(selector).get()
            if price_text:
                try:
                    # Clean and convert to float
                    price = price_text.replace('$', '').replace(',', '')
                    return float(price)
                except ValueError:
                    continue
        
        return 0.0
    
    def extract_rating(self, response):
        """Extract product rating"""
        rating_text = response.css('.a-icon-alt::text').re_first(r'(\d+\.?\d*) out of')
        if rating_text:
            try:
                return float(rating_text)
            except ValueError:
                pass
        return 0.0
    
    def extract_review_count(self, response):
        """Extract number of reviews"""
        review_text = response.css('#acrCustomerReviewText::text').get()
        if review_text:
            import re
            count = re.search(r'(\d+)', review_text.replace(',', ''))
            if count:
                return int(count.group(1))
        return 0
    
    def extract_description(self, response):
        """Extract product description"""
        # Try multiple description selectors
        desc_selectors = [
            '#feature-bullets ul li span::text',
            '#productDescription p::text',
            '.a-expander-content p::text'
        ]
        
        description_parts = []
        for selector in desc_selectors:
            parts = response.css(selector).getall()
            if parts:
                description_parts.extend([p.strip() for p in parts if p.strip()])
        
        return ' '.join(description_parts[:3])  # Limit length