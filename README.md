# AI-Powered Product Search Engine

An intelligent product search engine specializing in cosmetics, fashion, and healthcare products. This platform uses AI algorithms to scan e-commerce websites, analyze products, prices, and reviews to provide users with the best options at competitive prices.

## 🚀 Features

- **AI-Powered Search**: Intelligent product matching and query enhancement
- **Multi-Platform Scraping**: Automated data collection from major e-commerce sites
- **Price Comparison**: Real-time price tracking and deal detection
- **Sentiment Analysis**: AI-driven review analysis and sentiment scoring
- **Product Recommendations**: Similar product suggestions using ML algorithms
- **Category Specialization**: Focused on cosmetics, fashion, and healthcare products

## 🏗️ Architecture

### Backend (Python FastAPI)
- RESTful API with FastAPI
- PostgreSQL database with vector search
- AI/ML models for search enhancement
- Web scraping with Scrapy and Selenium
- Background task processing with Celery

### Frontend (React TypeScript)
- Modern React with TypeScript
- Responsive design with styled-components
- Real-time search with React Query
- Interactive product comparison
- Price history charts

### AI/ML Components
- Sentence Transformers for product similarity
- BERT-based sentiment analysis
- FAISS for vector similarity search
- Price prediction models

## 📁 Project Structure

```
AI Search/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── api/routes/     # API endpoints
│   │   ├── core/           # Configuration and database
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── scrapers/       # Web scraping modules
│   ├── main.py            # Application entry point
│   └── requirements.txt   # Python dependencies
├── frontend/              # React TypeScript frontend
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API clients
│   │   └── types/         # TypeScript definitions
│   └── package.json       # Node.js dependencies
├── ai-ml/                 # Machine learning models
│   ├── similarity_model.py
│   ├── sentiment_model.py
│   └── training_scripts/
├── database/              # Database schemas and migrations
│   ├── sample_data.sql
│   └── README.md
└── .github/              # GitHub configuration
    └── copilot-instructions.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+
- PostgreSQL 13+
- Redis (for background tasks)

### Backend Setup

1. **Create Python virtual environment**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup database**
   ```bash
   # Create PostgreSQL database
   createdb ai_search_db
   
   # Run migrations (if using Alembic)
   alembic upgrade head
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database and API keys
   ```

5. **Start the backend**
   ```bash
   python main.py
   ```

### Frontend Setup

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server**
   ```bash
   npm start
   ```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/ai_search_db

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Services
OPENAI_API_KEY=your-openai-api-key

# Redis
REDIS_URL=redis://localhost:6379

# CORS
ALLOWED_HOSTS=http://localhost:3000,http://127.0.0.1:3000
```

## 📊 Supported Websites

The platform currently supports scraping from:

- Amazon.com
- Sephora.com
- Ulta.com
- CVS.com
- Walgreens.com
- Target.com
- Walmart.com
- Nordstrom.com

## 🧪 API Endpoints

### Search
- `GET /api/search/products` - Search products with AI enhancement
- `GET /api/search/suggestions` - Get search suggestions
- `GET /api/search/trending` - Get trending products

### Products
- `GET /api/products/{id}` - Get product details
- `GET /api/products/{id}/reviews` - Get product reviews
- `GET /api/products/{id}/similar` - Get similar products
- `GET /api/products/{id}/price-history` - Get price history

### Scraper
- `POST /api/scraper/start-scraping` - Start scraping task
- `GET /api/scraper/supported-websites` - List supported sites

## 🤖 AI Features

### Search Enhancement
- Query expansion and refinement
- Synonym detection and replacement
- Category-aware search suggestions

### Product Similarity
- Text-based similarity using sentence transformers
- Feature-based matching
- Price and category consideration

### Sentiment Analysis
- Review sentiment scoring (-1 to 1)
- Product sentiment summaries
- Review quality assessment

## 🛠️ Development

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests  
cd frontend
npm test
```

### Code Formatting
```bash
# Backend
black backend/
flake8 backend/

# Frontend
cd frontend
npm run lint
```

### Adding New Scrapers

1. Create spider in `backend/app/scrapers/`
2. Implement website-specific parsing logic
3. Add to supported websites list
4. Test with sample data

## 📈 Performance Considerations

- Use Redis for caching frequent searches
- Implement pagination for large result sets
- Use background tasks for scraping operations
- Optimize database queries with proper indexing
- Consider CDN for static assets

## 🔒 Security

- Input validation on all API endpoints
- Rate limiting for search queries
- Secure authentication with JWT tokens
- HTTPS enforcement in production
- SQL injection prevention with ORM

## 🚀 Deployment

### Using Docker
```bash
# Build and run with docker-compose
docker-compose up -d
```

### Manual Deployment
1. Setup PostgreSQL and Redis servers
2. Configure environment variables
3. Build frontend: `npm run build`
4. Deploy backend with gunicorn
5. Serve frontend with nginx

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For questions or issues:
- Create an issue on GitHub
- Check the documentation in each module
- Review the API documentation at `/docs`

## 🔮 Future Enhancements

- Real-time price alerts
- User preference learning
- Mobile app development
- International marketplace support
- Advanced analytics dashboard
- Social media integration