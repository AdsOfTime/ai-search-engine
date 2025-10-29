from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.routes import products, search, auth, scraper, monetization, api_management
from app.core.config import settings
import os

app = FastAPI(
    title="AI Product Search Engine",
    description="AI-Powered Product Search Engine for Cosmetics, Fashion, and Healthcare",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(search.router, prefix="/api/search", tags=["search"])
app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(scraper.router, prefix="/api/scraper", tags=["scraper"])
app.include_router(monetization.router, prefix="/api/monetization", tags=["monetization"])
app.include_router(api_management.router, prefix="/api/apis", tags=["api_management"])

@app.get("/")
async def root():
    return {"message": "AI Product Search Engine API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    from app.core.database import SessionLocal
    from app.models.models import Product
    
    db = SessionLocal()
    try:
        product_count = db.query(Product).count()
        return {
            "status": "healthy", 
            "products_count": product_count,
            "message": "AI Product Search Engine is running"
        }
    finally:
        db.close()

@app.get("/demo")
async def serve_demo():
    demo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "demo.html")
    if os.path.exists(demo_path):
        return FileResponse(demo_path)
    return {"error": "Demo file not found"}

@app.get("/monetization")
async def serve_monetization_dashboard():
    dashboard_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "monetization-dashboard.html")
    if os.path.exists(dashboard_path):
        return FileResponse(dashboard_path)
    return {"error": "Monetization dashboard not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)