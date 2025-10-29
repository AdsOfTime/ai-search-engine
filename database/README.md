# Database Setup for AI Product Search Engine

This directory contains database schemas, migrations, and setup scripts.

## Database Schema

### Tables

1. **products** - Core product information
2. **reviews** - Customer reviews and ratings  
3. **search_queries** - Search analytics
4. **price_history** - Price tracking over time
5. **users** (optional) - User accounts
6. **categories** - Product categorization

## Setup Instructions

### PostgreSQL Setup

1. Install PostgreSQL 13+
2. Create database:
```sql
CREATE DATABASE ai_search_db;
CREATE USER ai_search_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE ai_search_db TO ai_search_user;
```

3. Run migrations:
```bash
cd backend
alembic upgrade head
```

### Environment Variables

Create `.env` file in backend directory:
```
DATABASE_URL=postgresql://ai_search_user:your_password@localhost/ai_search_db
```

## Vector Search Setup

For AI-powered similarity search, consider adding pgvector extension:

```sql
-- Install pgvector extension
CREATE EXTENSION vector;

-- Add vector column to products table
ALTER TABLE products ADD COLUMN embedding vector(384);

-- Create index for similarity search
CREATE INDEX ON products USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
```

## Sample Data

Use `sample_data.sql` to populate database with test products for development.