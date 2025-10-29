import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from typing import List, Dict, Tuple
import pickle
import os

class ProductSimilarityModel:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """Initialize the product similarity model"""
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.product_embeddings = None
        self.product_metadata = []
    
    def prepare_product_text(self, product: Dict) -> str:
        """Prepare product text for embedding"""
        text_parts = []
        
        # Add product name and brand
        if product.get('name'):
            text_parts.append(product['name'])
        if product.get('brand'):
            text_parts.append(f"Brand: {product['brand']}")
        
        # Add category information
        if product.get('category'):
            text_parts.append(f"Category: {product['category']}")
        if product.get('subcategory'):
            text_parts.append(f"Subcategory: {product['subcategory']}")
        
        # Add description
        if product.get('description'):
            # Limit description length to avoid very long texts
            desc = product['description'][:500]
            text_parts.append(desc)
        
        # Add features if available
        if product.get('features'):
            features = product['features']
            if isinstance(features, dict):
                for key, value in features.items():
                    if isinstance(value, (str, int, float)):
                        text_parts.append(f"{key}: {value}")
        
        return ' '.join(text_parts)
    
    def train_on_products(self, products: List[Dict]):
        """Train the similarity model on a list of products"""
        print(f"Training similarity model on {len(products)} products...")
        
        # Prepare text data
        product_texts = []
        self.product_metadata = []
        
        for product in products:
            text = self.prepare_product_text(product)
            product_texts.append(text)
            
            # Store metadata for retrieval
            self.product_metadata.append({
                'id': product.get('id'),
                'name': product.get('name'),
                'category': product.get('category'),
                'brand': product.get('brand'),
                'price': product.get('price'),
                'rating': product.get('rating')
            })
        
        # Generate embeddings
        print("Generating embeddings...")
        self.product_embeddings = self.model.encode(product_texts)
        
        # Build FAISS index for fast similarity search
        print("Building FAISS index...")
        dimension = self.product_embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)  # Inner product (cosine similarity)
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(self.product_embeddings)
        self.index.add(self.product_embeddings)
        
        print("Training completed!")
    
    def find_similar_products(self, target_product: Dict, k: int = 10) -> List[Tuple[Dict, float]]:
        """Find similar products to a target product"""
        if self.index is None:
            raise ValueError("Model not trained. Call train_on_products first.")
        
        # Generate embedding for target product
        target_text = self.prepare_product_text(target_product)
        target_embedding = self.model.encode([target_text])
        faiss.normalize_L2(target_embedding)
        
        # Search for similar products
        scores, indices = self.index.search(target_embedding, k + 1)  # +1 to exclude self
        
        # Prepare results
        results = []
        target_id = target_product.get('id')
        
        for score, idx in zip(scores[0], indices[0]):
            # Skip if it's the same product
            if self.product_metadata[idx].get('id') == target_id:
                continue
            
            similar_product = self.product_metadata[idx]
            similarity_score = float(score)
            results.append((similar_product, similarity_score))
        
        return results[:k]
    
    def find_similar_by_text(self, query_text: str, k: int = 10) -> List[Tuple[Dict, float]]:
        """Find products similar to a text query"""
        if self.index is None:
            raise ValueError("Model not trained. Call train_on_products first.")
        
        # Generate embedding for query
        query_embedding = self.model.encode([query_text])
        faiss.normalize_L2(query_embedding)
        
        # Search for similar products
        scores, indices = self.index.search(query_embedding, k)
        
        # Prepare results
        results = []
        for score, idx in zip(scores[0], indices[0]):
            similar_product = self.product_metadata[idx]
            similarity_score = float(score)
            results.append((similar_product, similarity_score))
        
        return results
    
    def save_model(self, model_path: str):
        """Save the trained model"""
        model_data = {
            'product_embeddings': self.product_embeddings,
            'product_metadata': self.product_metadata,
            'model_name': self.model.get_sentence_embedding_dimension()
        }
        
        with open(model_path, 'wb') as f:
            pickle.dump(model_data, f)
        
        # Save FAISS index
        faiss.write_index(self.index, model_path.replace('.pkl', '.faiss'))
        print(f"Model saved to {model_path}")
    
    def load_model(self, model_path: str):
        """Load a trained model"""
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        
        self.product_embeddings = model_data['product_embeddings']
        self.product_metadata = model_data['product_metadata']
        
        # Load FAISS index
        faiss_path = model_path.replace('.pkl', '.faiss')
        if os.path.exists(faiss_path):
            self.index = faiss.read_index(faiss_path)
        
        print(f"Model loaded from {model_path}")

def train_similarity_model(products_data: List[Dict], save_path: str = 'models/similarity_model.pkl'):
    """Train and save a product similarity model"""
    model = ProductSimilarityModel()
    model.train_on_products(products_data)
    
    # Create models directory if it doesn't exist
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    model.save_model(save_path)
    
    return model

if __name__ == "__main__":
    # Example usage
    sample_products = [
        {
            'id': 1,
            'name': 'Moisturizing Face Cream',
            'brand': 'CeraVe',
            'category': 'skincare',
            'subcategory': 'moisturizer',
            'description': 'Daily facial moisturizer with hyaluronic acid',
            'price': 15.99,
            'rating': 4.5
        },
        {
            'id': 2, 
            'name': 'Hydrating Serum',
            'brand': 'The Ordinary',
            'category': 'skincare',
            'subcategory': 'serum',
            'description': 'Hyaluronic acid serum for deep hydration',
            'price': 12.90,
            'rating': 4.3
        }
    ]
    
    model = train_similarity_model(sample_products)
    
    # Test similarity
    similar = model.find_similar_products(sample_products[0], k=5)
    print("Similar products:", similar)