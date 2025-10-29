#!/usr/bin/env python3
"""
Database Initialization Script
Creates all database tables and sets up the database schema
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine, Base
from app.models.models import Product, Review, SearchQuery, PriceHistory

def init_database():
    """Initialize the database with all tables"""
    try:
        print("🗄️ Initializing AI Product Search Engine Database...")
        print("=" * 50)
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        print("✅ Database tables created successfully!")
        print("\nCreated tables:")
        print("• products - Store product information")
        print("• reviews - Customer reviews and ratings") 
        print("• search_queries - Search analytics")
        print("• price_history - Price tracking over time")
        
        return True
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

if __name__ == "__main__":
    success = init_database()
    if success:
        print("\n🎉 Database is ready for use!")
    else:
        print("\n💥 Database initialization failed!")
        sys.exit(1)