#!/usr/bin/env python3
"""
Complete Setup Script for AI Product Search Engine
Initializes database, populates with sample and real data
"""

import asyncio
import sys
import os
from pathlib import Path

# Add backend to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

async def main():
    """Main setup function"""
    print("🚀 AI Product Search Engine - Complete Setup")
    print("=" * 50)
    
    try:
        # Step 1: Initialize Database
        print("\n1️⃣ Initializing Database...")
        from init_db import init_database
        if not init_database():
            raise Exception("Database initialization failed")
        
        # Step 2: Install required packages
        print("\n2️⃣ Installing required packages...")
        import subprocess
        packages = [
            "aiohttp",
            "beautifulsoup4", 
            "requests",
            "selenium"
        ]
        
        for package in packages:
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"   ✅ {package}")
            except subprocess.CalledProcessError:
                print(f"   ⚠️ {package} (already installed or failed)")
        
        # Step 3: Populate with sample data
        print("\n3️⃣ Generating sample products...")
        from populate_sample_data import SampleDataGenerator
        
        generator = SampleDataGenerator()
        await generator.populate_products(count_per_category=20)
        
        # Step 4: Scrape real data
        print("\n4️⃣ Scraping real product data...")
        from scrape_real_data import RealProductScraper
        
        scraper = RealProductScraper()
        try:
            await scraper.scrape_fake_store_api()
            await scraper.scrape_makeup_api()
            await scraper.scrape_nutrition_api()
        finally:
            await scraper.close()
        
        # Step 5: Verify setup
        print("\n5️⃣ Verifying setup...")
        from sqlalchemy.orm import sessionmaker
        from app.core.database import engine
        from app.models.models import Product
        
        Session = sessionmaker(bind=engine)
        session = Session()
        
        try:
            total_products = session.query(Product).count()
            cosmetics_count = session.query(Product).filter(Product.category == 'cosmetics').count()
            fashion_count = session.query(Product).filter(Product.category == 'fashion').count()
            healthcare_count = session.query(Product).filter(Product.category == 'healthcare').count()
            
            print(f"   ✅ Total products: {total_products}")
            print(f"   ✅ Cosmetics: {cosmetics_count}")
            print(f"   ✅ Fashion: {fashion_count}")
            print(f"   ✅ Healthcare: {healthcare_count}")
            
        finally:
            session.close()
        
        print("\n🎉 Setup completed successfully!")
        print("\nYour AI Product Search Engine now has:")
        print("• Fully initialized database with all tables")
        print("• Sample product data across all categories")
        print("• Real product data from external APIs")
        print("• Reviews and price history")
        print("• Search analytics ready")
        
        print(f"\n🚀 Start your servers:")
        print("Backend: python main.py (Port 8002)")
        print("Demo: python -m http.server 3000")
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        print("Please check the error above and try again.")
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(main())
    if not success:
        sys.exit(1)