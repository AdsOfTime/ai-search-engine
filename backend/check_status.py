#!/usr/bin/env python3
"""
AI Product Search Engine - Status Check & Next Steps
This script verifies that everything is working and shows you what to do next.
"""

import requests
import json
from datetime import datetime

def test_backend():
    """Test if backend API is responding"""
    try:
        # Test health endpoint
        health = requests.get("http://localhost:8002/health", timeout=5)
        if health.status_code == 200:
            print("✅ Backend API is healthy")
        else:
            print("❌ Backend API health check failed")
            return False
        
        # Test search endpoint
        search = requests.get("http://localhost:8002/api/search/products?q=primer", timeout=5)
        if search.status_code == 200:
            data = search.json()
            print(f"✅ Search API working - Found {data.get('total', 0)} products")
            if data.get('products'):
                sample = data['products'][0]
                print(f"   Sample: {sample.get('name', 'Unknown')} by {sample.get('brand', 'Unknown')} - ${sample.get('price', 0)}")
        else:
            print("❌ Search API failed")
            return False
            
        # Test categories
        categories = ['cosmetics', 'fashion', 'healthcare']
        for category in categories:
            cat_search = requests.get(f"http://localhost:8002/api/search/products?q=product&category={category}", timeout=5)
            if cat_search.status_code == 200:
                cat_data = cat_search.json()
                print(f"✅ {category.title()}: {cat_data.get('total', 0)} products")
            else:
                print(f"❌ {category.title()}: API error")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend - make sure it's running on port 8002")
        return False
    except Exception as e:
        print(f"❌ Backend test error: {e}")
        return False

def test_frontend():
    """Test if frontend demo is accessible"""
    try:
        demo = requests.get("http://localhost:3000/demo.html", timeout=5)
        if demo.status_code == 200:
            print("✅ Demo frontend is accessible")
            return True
        else:
            print("❌ Demo frontend failed")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to demo - make sure server is running on port 3000")
        return False
    except Exception as e:
        print(f"❌ Frontend test error: {e}")
        return False

def show_next_steps():
    """Show what to do next"""
    print("\n🎯 WHAT TO DO NEXT:")
    print("=" * 50)
    
    print("\n1. 🔍 TEST YOUR SEARCH ENGINE:")
    print("   • Open: http://localhost:3000/demo.html")
    print("   • Try searching for: 'primer', 'vitamin', 'dress'")
    print("   • Click category buttons to browse by type")
    
    print("\n2. 📊 EXPLORE THE API:")
    print("   • API Documentation: http://localhost:8002/docs")
    print("   • Try different endpoints and filters")
    print("   • Test search parameters and sorting")
    
    print("\n3. 🚀 ADD MORE PRODUCTS:")
    print("   • Run: python scrape_real_data.py (adds real products)")
    print("   • Run: python populate_sample_data.py (adds sample products)")
    print("   • Edit these scripts to add your own data sources")
    
    print("\n4. 🎨 CUSTOMIZE THE INTERFACE:")
    print("   • Edit demo.html to change the look and feel")
    print("   • Add new search features and filters")
    print("   • Connect to your own frontend framework")
    
    print("\n5. 🧠 ENHANCE AI FEATURES:")
    print("   • Implement the AI similarity search")
    print("   • Add sentiment analysis for reviews")
    print("   • Create product recommendations")
    
    print("\n6. 📈 SCALE FOR PRODUCTION:")
    print("   • Switch from SQLite to PostgreSQL")
    print("   • Add Redis for caching")
    print("   • Implement user authentication")
    print("   • Deploy to cloud platforms")

def main():
    print("🚀 AI PRODUCT SEARCH ENGINE - STATUS CHECK")
    print("=" * 55)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n🔧 TESTING COMPONENTS...")
    
    backend_ok = test_backend()
    frontend_ok = test_frontend()
    
    print(f"\n📊 SYSTEM STATUS:")
    print(f"Backend API: {'🟢 RUNNING' if backend_ok else '🔴 OFFLINE'}")
    print(f"Frontend Demo: {'🟢 RUNNING' if frontend_ok else '🔴 OFFLINE'}")
    
    if backend_ok and frontend_ok:
        print("\n🎉 SUCCESS! Your AI Product Search Engine is fully operational!")
        show_next_steps()
    else:
        print("\n⚠️ Some components need attention:")
        if not backend_ok:
            print("   • Start backend: cd backend; .\\venv\\Scripts\\Activate.ps1; python main.py")
        if not frontend_ok:
            print("   • Start frontend: cd C:\\AI Search; python -m http.server 3000")

if __name__ == "__main__":
    main()