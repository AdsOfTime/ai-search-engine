import openai
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.models import Product, Review
import asyncio
import json

class AIService:
    def __init__(self):
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
    
    async def enhance_search_query(self, query: str, category: Optional[str] = None) -> str:
        """Use AI to enhance and expand search queries"""
        try:
            if not settings.OPENAI_API_KEY:
                return query
            
            prompt = f"""
            Enhance this product search query to be more specific and comprehensive.
            Original query: "{query}"
            Category: {category or "any"}
            
            Rules:
            1. Keep the original intent
            2. Add relevant synonyms and variations
            3. Consider common product attributes
            4. Return only the enhanced query, no explanation
            
            Enhanced query:
            """
            
            response = await openai.Completion.acreate(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=100,
                temperature=0.3
            )
            
            enhanced = response.choices[0].text.strip()
            return enhanced if enhanced else query
            
        except Exception as e:
            # Fallback to original query if AI enhancement fails
            print(f"AI enhancement error: {e}")
            return query
    
    async def analyze_review_sentiment(self, review_text: str) -> float:
        """Analyze sentiment of product reviews"""
        try:
            if not settings.OPENAI_API_KEY:
                return 0.0
            
            prompt = f"""
            Analyze the sentiment of this product review and return a score between -1 and 1.
            -1 = very negative, 0 = neutral, 1 = very positive
            
            Review: "{review_text}"
            
            Return only the numerical score:
            """
            
            response = await openai.Completion.acreate(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=10,
                temperature=0.1
            )
            
            score = float(response.choices[0].text.strip())
            return max(-1, min(1, score))  # Ensure score is within bounds
            
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return 0.0
    
    async def find_similar_products(self, product: Product, limit: int, db: Session) -> List[Product]:
        """Find similar products using AI similarity matching"""
        try:
            # Simple similarity based on category, brand, and price range
            similar_products = (
                db.query(Product)
                .filter(
                    Product.id != product.id,
                    Product.category == product.category,
                    Product.in_stock == True,
                    Product.price >= product.price * 0.7,
                    Product.price <= product.price * 1.3
                )
                .order_by(Product.rating.desc())
                .limit(limit)
                .all()
            )
            
            # TODO: Implement more sophisticated AI-based similarity
            # This could include:
            # - Text similarity using embeddings
            # - Feature matching
            # - User behavior analysis
            
            return similar_products
            
        except Exception as e:
            print(f"Similar products error: {e}")
            return []
    
    async def extract_product_features(self, product_text: str) -> Dict:
        """Extract key features from product description using AI"""
        try:
            if not settings.OPENAI_API_KEY:
                return {}
            
            prompt = f"""
            Extract key product features from this description and return as JSON.
            Focus on: ingredients, benefits, size/volume, color, material, brand claims.
            
            Product description: "{product_text}"
            
            Return JSON format:
            """
            
            response = await openai.Completion.acreate(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=200,
                temperature=0.2
            )
            
            features_json = response.choices[0].text.strip()
            return json.loads(features_json)
            
        except Exception as e:
            print(f"Feature extraction error: {e}")
            return {}
    
    async def generate_product_summary(self, product: Product, reviews: List[Review]) -> str:
        """Generate AI-powered product summary based on product details and reviews"""
        try:
            if not settings.OPENAI_API_KEY:
                return f"{product.name} - {product.description[:200]}..."
            
            # Prepare review samples
            review_samples = [r.review_text for r in reviews[:5] if r.review_text]
            reviews_text = " | ".join(review_samples)
            
            prompt = f"""
            Create a concise product summary based on product info and customer reviews.
            
            Product: {product.name}
            Category: {product.category}
            Brand: {product.brand}
            Price: ${product.price}
            Rating: {product.rating}/5 ({product.review_count} reviews)
            
            Recent reviews: {reviews_text}
            
            Generate a 2-3 sentence summary highlighting key benefits and customer sentiment:
            """
            
            response = await openai.Completion.acreate(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=150,
                temperature=0.4
            )
            
            return response.choices[0].text.strip()
            
        except Exception as e:
            print(f"Summary generation error: {e}")
            return f"{product.name} - A {product.category} product from {product.brand}."