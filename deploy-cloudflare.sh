#!/bin/bash
# Cloudflare Deployment Script for AI Search Engine
# Run this script to deploy both frontend and backend to Cloudflare

set -e

echo "🚀 Starting Cloudflare deployment for AI Search Engine..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if wrangler is installed
if ! command -v wrangler &> /dev/null; then
    echo -e "${RED}❌ Wrangler CLI not found. Installing...${NC}"
    npm install -g wrangler
fi

# Login check
echo -e "${YELLOW}🔐 Checking Cloudflare authentication...${NC}"
if ! wrangler whoami &> /dev/null; then
    echo -e "${YELLOW}Please login to Cloudflare:${NC}"
    wrangler login
fi

# Function to create D1 database
create_database() {
    echo -e "${YELLOW}📊 Setting up Cloudflare D1 database...${NC}"
    
    # Create D1 database
    DATABASE_ID=$(wrangler d1 create ai-search-db --output json | jq -r '.id' 2>/dev/null || echo "")
    
    if [ -z "$DATABASE_ID" ]; then
        echo -e "${RED}❌ Failed to create D1 database${NC}"
        echo "Please create the database manually:"
        echo "wrangler d1 create ai-search-db"
        read -p "Enter your D1 database ID: " DATABASE_ID
    fi
    
    echo -e "${GREEN}✅ Database created with ID: $DATABASE_ID${NC}"
    
    # Update wrangler.toml with database ID
    if [ -f "wrangler.toml" ]; then
        sed -i "s/your-d1-database-id/$DATABASE_ID/g" wrangler.toml
        echo -e "${GREEN}✅ Updated wrangler.toml with database ID${NC}"
    fi
    
    # Run database schema
    echo -e "${YELLOW}📋 Applying database schema...${NC}"
    wrangler d1 execute ai-search-db --file=cloudflare-d1-schema.sql
    echo -e "${GREEN}✅ Database schema applied${NC}"
}

# Function to create KV namespace
create_kv_namespace() {
    echo -e "${YELLOW}🗂️ Creating KV namespace for caching...${NC}"
    
    KV_ID=$(wrangler kv:namespace create "AI_SEARCH_CACHE" --output json | jq -r '.id' 2>/dev/null || echo "")
    
    if [ -z "$KV_ID" ]; then
        echo -e "${RED}❌ Failed to create KV namespace${NC}"
        read -p "Enter your KV namespace ID: " KV_ID
    fi
    
    echo -e "${GREEN}✅ KV namespace created with ID: $KV_ID${NC}"
    
    # Update wrangler.toml
    if [ -f "wrangler.toml" ]; then
        sed -i "s/your-kv-namespace-id/$KV_ID/g" wrangler.toml
    fi
}

# Function to set secrets
set_secrets() {
    echo -e "${YELLOW}🔑 Setting up environment secrets...${NC}"
    
    echo "Enter your secrets (press Enter to skip):"
    
    read -p "OpenAI API Key: " -s OPENAI_KEY
    if [ ! -z "$OPENAI_KEY" ]; then
        echo "$OPENAI_KEY" | wrangler secret put OPENAI_API_KEY
        echo -e "${GREEN}✅ OpenAI API key set${NC}"
    fi
    
    read -p "Database URL (external): " DATABASE_URL
    if [ ! -z "$DATABASE_URL" ]; then
        echo "$DATABASE_URL" | wrangler secret put DATABASE_URL
        echo -e "${GREEN}✅ Database URL set${NC}"
    fi
    
    read -p "Secret Key: " -s SECRET_KEY
    if [ ! -z "$SECRET_KEY" ]; then
        echo "$SECRET_KEY" | wrangler secret put SECRET_KEY
        echo -e "${GREEN}✅ Secret key set${NC}"
    fi
}

# Function to deploy worker
deploy_worker() {
    echo -e "${YELLOW}🛠️ Building and deploying Cloudflare Worker...${NC}"
    
    cd cloudflare-workers
    
    # Install dependencies
    if [ ! -d "node_modules" ]; then
        npm install
    fi
    
    # Deploy worker
    wrangler publish
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Worker deployed successfully${NC}"
    else
        echo -e "${RED}❌ Worker deployment failed${NC}"
        exit 1
    fi
    
    cd ..
}

# Function to deploy frontend
deploy_frontend() {
    echo -e "${YELLOW}🌐 Deploying frontend to Cloudflare Pages...${NC}"
    
    cd frontend
    
    # Install dependencies if not exists
    if [ ! -d "node_modules" ]; then
        npm install
    fi
    
    # Build frontend
    npm run build
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Frontend built successfully${NC}"
        
        # Deploy to Cloudflare Pages
        echo -e "${YELLOW}📤 Deploying to Cloudflare Pages...${NC}"
        echo "Please connect your GitHub repository to Cloudflare Pages:"
        echo "1. Go to https://dash.cloudflare.com/pages"
        echo "2. Click 'Create a project'"
        echo "3. Connect your GitHub repository"
        echo "4. Set build command: npm run build"
        echo "5. Set build output directory: build"
        echo "6. Set root directory: frontend"
        
        read -p "Press Enter after setting up Cloudflare Pages connection..."
        
    else
        echo -e "${RED}❌ Frontend build failed${NC}"
        exit 1
    fi
    
    cd ..
}

# Function to migrate data
migrate_data() {
    echo -e "${YELLOW}📦 Migrating existing data to Cloudflare D1...${NC}"
    
    # Check if scraped data exists
    if [ -f "backend/scraped_products_*.csv" ]; then
        echo "Found scraped product data. Converting to D1..."
        
        # Create data migration script
        python3 << EOF
import csv
import json
import sqlite3
import uuid
from pathlib import glob

# Find the latest scraped data file
csv_files = glob("backend/scraped_products_*.csv")
if csv_files:
    latest_file = max(csv_files)
    print(f"Processing: {latest_file}")
    
    # Generate SQL inserts
    with open(latest_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        sql_statements = []
        for row in reader:
            product_id = str(uuid.uuid4())
            
            # Clean and format data
            name = row.get('name', '').replace("'", "''")
            brand = row.get('brand', '').replace("'", "''")
            category = row.get('category', 'general').replace("'", "''")
            price = float(row.get('price', 0)) if row.get('price') else 0
            rating = float(row.get('rating', 0)) if row.get('rating') else 0
            description = row.get('description', '').replace("'", "''")[:500]
            
            sql = f"""
            INSERT INTO products (id, name, brand, category, price, rating, description, in_stock)
            VALUES ('{product_id}', '{name}', '{brand}', '{category}', {price}, {rating}, '{description}', 1);
            """
            sql_statements.append(sql)
    
    # Write migration file
    with open('data_migration.sql', 'w') as f:
        f.write('\n'.join(sql_statements))
    
    print("✅ Data migration SQL generated: data_migration.sql")
else:
    print("No scraped data found")
EOF
        
        # Apply migration if file was created
        if [ -f "data_migration.sql" ]; then
            wrangler d1 execute ai-search-db --file=data_migration.sql
            echo -e "${GREEN}✅ Data migrated successfully${NC}"
            rm data_migration.sql
        fi
    else
        echo "No existing data to migrate"
    fi
}

# Function to test deployment
test_deployment() {
    echo -e "${YELLOW}🧪 Testing deployment...${NC}"
    
    # Get worker URL
    WORKER_URL=$(wrangler whoami | grep -o 'https://.*\.workers\.dev' | head -1)
    
    if [ ! -z "$WORKER_URL" ]; then
        echo "Testing API endpoints..."
        
        # Test health endpoint
        curl -s "$WORKER_URL/api/health" | jq .
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ API is responding correctly${NC}"
        else
            echo -e "${RED}❌ API test failed${NC}"
        fi
    fi
}

# Main deployment flow
main() {
    echo -e "${GREEN}🔧 AI Search Engine - Cloudflare Deployment${NC}"
    echo "======================================"
    
    # Check if required files exist
    if [ ! -f "wrangler.toml" ]; then
        echo -e "${RED}❌ wrangler.toml not found${NC}"
        exit 1
    fi
    
    # Menu for deployment options
    echo "Select deployment option:"
    echo "1) Full deployment (database + worker + frontend)"
    echo "2) Backend only (database + worker)"
    echo "3) Frontend only"
    echo "4) Database setup only"
    echo "5) Migrate data only"
    
    read -p "Choose option (1-5): " choice
    
    case $choice in
        1)
            create_database
            create_kv_namespace
            set_secrets
            migrate_data
            deploy_worker
            deploy_frontend
            test_deployment
            ;;
        2)
            create_database
            create_kv_namespace
            set_secrets
            migrate_data
            deploy_worker
            test_deployment
            ;;
        3)
            deploy_frontend
            ;;
        4)
            create_database
            create_kv_namespace
            ;;
        5)
            migrate_data
            ;;
        *)
            echo "Invalid option"
            exit 1
            ;;
    esac
    
    echo -e "${GREEN}🎉 Deployment completed!${NC}"
    echo ""
    echo -e "${YELLOW}📋 Next steps:${NC}"
    echo "1. Update your frontend API URLs to point to the worker"
    echo "2. Set up custom domain in Cloudflare"
    echo "3. Configure DNS records"
    echo "4. Test all functionality"
    echo ""
    echo -e "${GREEN}🔗 Useful links:${NC}"
    echo "• Cloudflare Dashboard: https://dash.cloudflare.com"
    echo "• Workers & Pages: https://dash.cloudflare.com/pages"
    echo "• D1 Database: https://dash.cloudflare.com/d1"
}

# Run main function
main "$@"