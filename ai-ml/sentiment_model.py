from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import List, Dict
import numpy as np

class SentimentAnalyzer:
    def __init__(self, model_name: str = 'cardiffnlp/twitter-roberta-base-sentiment-latest'):
        """Initialize sentiment analyzer with pre-trained model"""
        self.model_name = model_name
        self.sentiment_pipeline = None
        self._load_model()
    
    def _load_model(self):
        """Load the pre-trained sentiment model"""
        try:
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model=self.model_name,
                tokenizer=self.model_name,
                device=0 if torch.cuda.is_available() else -1
            )
            print(f"Loaded sentiment model: {self.model_name}")
        except Exception as e:
            print(f"Error loading model {self.model_name}: {e}")
            # Fallback to basic model
            self.sentiment_pipeline = pipeline("sentiment-analysis")
    
    def analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment of a single text"""
        if not text or not text.strip():
            return {'label': 'NEUTRAL', 'score': 0.5, 'normalized_score': 0.0}
        
        try:
            # Clean text
            cleaned_text = self._clean_text(text)
            
            # Get sentiment prediction
            result = self.sentiment_pipeline(cleaned_text)[0]
            
            # Normalize score to -1 to 1 range
            normalized_score = self._normalize_score(result)
            
            return {
                'label': result['label'],
                'confidence': result['score'],
                'normalized_score': normalized_score,
                'text_length': len(text)
            }
            
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return {'label': 'NEUTRAL', 'score': 0.5, 'normalized_score': 0.0}
    
    def analyze_batch(self, texts: List[str]) -> List[Dict]:
        """Analyze sentiment for multiple texts"""
        results = []
        for text in texts:
            results.append(self.analyze_sentiment(text))
        return results
    
    def analyze_product_reviews(self, reviews: List[Dict]) -> Dict:
        """Analyze sentiment for product reviews and provide summary"""
        if not reviews:
            return {
                'average_sentiment': 0.0,
                'sentiment_distribution': {'positive': 0, 'neutral': 0, 'negative': 0},
                'total_reviews': 0
            }
        
        sentiments = []
        sentiment_counts = {'positive': 0, 'neutral': 0, 'negative': 0}
        
        for review in reviews:
            review_text = review.get('review_text', '') or review.get('text', '')
            if not review_text:
                continue
                
            sentiment_result = self.analyze_sentiment(review_text)
            normalized_score = sentiment_result['normalized_score']
            sentiments.append(normalized_score)
            
            # Count sentiment categories
            if normalized_score > 0.1:
                sentiment_counts['positive'] += 1
            elif normalized_score < -0.1:
                sentiment_counts['negative'] += 1
            else:
                sentiment_counts['neutral'] += 1
        
        average_sentiment = np.mean(sentiments) if sentiments else 0.0
        
        return {
            'average_sentiment': float(average_sentiment),
            'sentiment_distribution': sentiment_counts,
            'total_reviews': len(sentiments),
            'sentiment_breakdown': {
                'positive_percentage': sentiment_counts['positive'] / len(sentiments) * 100 if sentiments else 0,
                'neutral_percentage': sentiment_counts['neutral'] / len(sentiments) * 100 if sentiments else 0,
                'negative_percentage': sentiment_counts['negative'] / len(sentiments) * 100 if sentiments else 0
            }
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean text for sentiment analysis"""
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Limit text length (models have token limits)
        max_length = 512
        if len(text) > max_length:
            text = text[:max_length]
        
        return text
    
    def _normalize_score(self, result: Dict) -> float:
        """Normalize sentiment score to -1 to 1 range"""
        label = result['label'].upper()
        confidence = result['score']
        
        # Map different model outputs to normalized score
        if 'POSITIVE' in label or 'POS' in label:
            return confidence  # 0 to 1
        elif 'NEGATIVE' in label or 'NEG' in label:
            return -confidence  # 0 to -1
        else:  # NEUTRAL
            return 0.0

class ReviewAnalyzer:
    """Specialized analyzer for product reviews"""
    
    def __init__(self):
        self.sentiment_analyzer = SentimentAnalyzer()
    
    def analyze_review_quality(self, review: Dict) -> Dict:
        """Analyze review quality and helpfulness"""
        review_text = review.get('review_text', '') or review.get('text', '')
        
        if not review_text:
            return {'quality_score': 0.0, 'is_helpful': False}
        
        # Basic quality metrics
        word_count = len(review_text.split())
        has_specific_details = any(keyword in review_text.lower() for keyword in [
            'ingredients', 'texture', 'color', 'size', 'quality', 'packaging',
            'delivery', 'shipping', 'recommend', 'worth', 'price'
        ])
        
        # Sentiment analysis
        sentiment = self.sentiment_analyzer.analyze_sentiment(review_text)
        
        # Quality score calculation
        quality_score = 0.0
        
        # Length factor (reviews with 10-200 words are typically more helpful)
        if 10 <= word_count <= 200:
            quality_score += 0.4
        elif word_count > 200:
            quality_score += 0.2
        
        # Specific details factor
        if has_specific_details:
            quality_score += 0.3
        
        # Verified purchase factor
        if review.get('verified_purchase', False):
            quality_score += 0.2
        
        # Helpful votes factor
        helpful_votes = review.get('helpful_votes', 0)
        if helpful_votes > 0:
            quality_score += min(0.1, helpful_votes / 10)  # Cap at 0.1
        
        is_helpful = quality_score >= 0.5 and word_count >= 10
        
        return {
            'quality_score': min(1.0, quality_score),
            'is_helpful': is_helpful,
            'word_count': word_count,
            'has_specific_details': has_specific_details,
            'sentiment': sentiment
        }
    
    def get_review_insights(self, reviews: List[Dict]) -> Dict:
        """Get comprehensive insights from product reviews"""
        if not reviews:
            return {}
        
        # Analyze all reviews
        review_analyses = []
        for review in reviews:
            analysis = self.analyze_review_quality(review)
            review_analyses.append(analysis)
        
        # Get sentiment summary
        sentiment_summary = self.sentiment_analyzer.analyze_product_reviews(reviews)
        
        # Calculate quality metrics
        quality_scores = [r['quality_score'] for r in review_analyses]
        helpful_reviews = [r for r in review_analyses if r['is_helpful']]
        
        # Extract common themes (simplified)
        all_review_text = ' '.join([
            r.get('review_text', '') or r.get('text', '') 
            for r in reviews if r.get('review_text') or r.get('text')
        ])
        
        common_words = self._extract_common_themes(all_review_text)
        
        return {
            'sentiment_summary': sentiment_summary,
            'quality_metrics': {
                'average_quality_score': np.mean(quality_scores) if quality_scores else 0.0,
                'helpful_reviews_count': len(helpful_reviews),
                'helpful_reviews_percentage': len(helpful_reviews) / len(reviews) * 100 if reviews else 0
            },
            'common_themes': common_words,
            'total_reviews_analyzed': len(reviews)
        }
    
    def _extract_common_themes(self, text: str) -> List[str]:
        """Extract common themes from review text (simplified version)"""
        if not text:
            return []
        
        # Common positive/negative words in cosmetic/fashion/healthcare reviews
        positive_themes = ['love', 'great', 'amazing', 'perfect', 'recommend', 'excellent', 'beautiful']
        negative_themes = ['terrible', 'awful', 'waste', 'disappointed', 'broke', 'cheap', 'horrible']
        
        text_lower = text.lower()
        found_themes = []
        
        for theme in positive_themes + negative_themes:
            if theme in text_lower:
                found_themes.append(theme)
        
        return list(set(found_themes))[:10]  # Return unique themes, limit to 10

if __name__ == "__main__":
    # Example usage
    analyzer = SentimentAnalyzer()
    
    sample_reviews = [
        {'review_text': 'This product is amazing! I love the texture and it works great.', 'verified_purchase': True},
        {'review_text': 'Terrible quality, waste of money. Would not recommend.', 'verified_purchase': False},
        {'review_text': 'It\'s okay, nothing special but does the job.', 'verified_purchase': True}
    ]
    
    # Analyze individual sentiment
    for review in sample_reviews:
        sentiment = analyzer.analyze_sentiment(review['review_text'])
        print(f"Review: {review['review_text'][:50]}...")
        print(f"Sentiment: {sentiment}")
        print()
    
    # Analyze product reviews summary
    review_analyzer = ReviewAnalyzer()
    insights = review_analyzer.get_review_insights(sample_reviews)
    print("Review Insights:", insights)