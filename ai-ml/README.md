# AI/ML Models and Training Scripts for Product Search Engine

## Overview
This directory contains machine learning models and training scripts for:
1. Product similarity matching
2. Review sentiment analysis  
3. Price prediction
4. Search query enhancement
5. Product categorization

## Models

### 1. Product Similarity Model
- **File**: `similarity_model.py`
- **Purpose**: Find similar products based on features, descriptions, and user behavior
- **Technology**: Sentence Transformers, FAISS for vector search
- **Input**: Product descriptions, features, category
- **Output**: Similarity scores and recommendations

### 2. Sentiment Analysis Model
- **File**: `sentiment_model.py` 
- **Purpose**: Analyze customer review sentiment
- **Technology**: Fine-tuned BERT or RoBERTa model
- **Input**: Review text
- **Output**: Sentiment score (-1 to 1)

### 3. Price Prediction Model
- **File**: `price_model.py`
- **Purpose**: Predict optimal pricing and detect deals
- **Technology**: XGBoost or Random Forest
- **Input**: Product features, historical prices, competitor data
- **Output**: Price predictions and deal scores

### 4. Search Enhancement Model
- **File**: `search_model.py`
- **Purpose**: Enhance user search queries
- **Technology**: GPT-based query expansion
- **Input**: User search query, search context
- **Output**: Enhanced search terms and filters

## Training Data
- Product descriptions and features
- Historical price data
- Customer reviews and ratings
- User search patterns
- Category hierarchies

## Usage
```bash
# Install dependencies
pip install -r requirements.txt

# Train similarity model
python train_similarity_model.py

# Train sentiment model  
python train_sentiment_model.py

# Evaluate models
python evaluate_models.py
```