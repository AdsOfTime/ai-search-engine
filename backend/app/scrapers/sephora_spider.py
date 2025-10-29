import scrapy

class SephoraProductSpider(scrapy.Spider):
    name = "sephora_products"
    allowed_domains = ["sephora.com"]
    
    def __init__(self, category="makeup", *args, **kwargs):
        super(SephoraProductSpider, self).__init__(*args, **kwargs)
        self.category = category
        
        # Sephora category URLs
        category_urls = {
            "makeup": "https://www.sephora.com/shop/makeup",
            "skincare": "https://www.sephora.com/shop/skincare",
            "fragrance": "https://www.sephora.com/shop/fragrance",
            "hair": "https://www.sephora.com/shop/hair"
        }
        
        self.start_urls = [category_urls.get(category, category_urls["makeup"])]
    
    def parse(self, response):
        """Parse category page for product links"""
        # Sephora uses JavaScript, so this is a simplified example
        product_urls = response.css('[data-comp="ProductTile"] a::attr(href)').getall()
        
        for url in product_urls[:20]:  # Limit for demo
            if url:
                full_url = response.urljoin(url)
                yield response.follow(full_url, self.parse_product)
    
    def parse_product(self, response):
        """Parse individual product page"""
        yield {
            'name': response.css('[data-at="product_name"]::text').get(),
            'price': self.extract_price(response),
            'rating': self.extract_rating(response),
            'review_count': self.extract_review_count(response),
            'description': self.extract_description(response),
            'image_url': response.css('.image-gallery img::attr(src)').get(),
            'product_url': response.url,
            'category': 'cosmetics',
            'source_website': 'sephora.com',
            'brand': response.css('[data-at="brand_name"]::text').get(),
            'in_stock': not response.css('.out-of-stock').get()
        }
    
    def extract_price(self, response):
        """Extract price from Sephora product page"""
        price_text = response.css('[data-at="price"]::text').get()
        if price_text:
            try:
                price = price_text.replace('$', '').replace(',', '')
                return float(price)
            except ValueError:
                pass
        return 0.0
    
    def extract_rating(self, response):
        """Extract rating from Sephora product page"""
        rating_text = response.css('[data-at="rating"]::attr(aria-label)').get()
        if rating_text:
            import re
            rating = re.search(r'(\d+\.?\d*)', rating_text)
            if rating:
                return float(rating.group(1))
        return 0.0
    
    def extract_review_count(self, response):
        """Extract review count from Sephora product page"""
        review_text = response.css('[data-at="number_of_reviews"]::text').get()
        if review_text:
            import re
            count = re.search(r'(\d+)', review_text.replace(',', ''))
            if count:
                return int(count.group(1))
        return 0
    
    def extract_description(self, response):
        """Extract product description"""
        description = response.css('[data-at="product_description"] p::text').get()
        return description.strip() if description else ''