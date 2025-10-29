from fastapi import APIRouter, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db

router = APIRouter()

@router.post("/start-scraping")
async def start_scraping(
    websites: List[str],
    categories: List[str],
    background_tasks: BackgroundTasks
):
    """Start web scraping task"""
    from app.services.scraper_service import ScraperService
    
    scraper_service = ScraperService()
    
    # Add scraping task to background
    background_tasks.add_task(
        scraper_service.scrape_websites,
        websites,
        categories
    )
    
    return {
        "message": "Scraping task started",
        "websites": websites,
        "categories": categories
    }

@router.get("/scraping-status")
async def get_scraping_status():
    """Get status of current scraping tasks"""
    # Implement scraping status tracking
    return {"message": "Scraping status endpoint - implement status tracking"}

@router.get("/supported-websites")
async def get_supported_websites():
    """Get list of supported e-commerce websites"""
    supported_sites = [
        "amazon.com",
        "sephora.com",
        "ulta.com", 
        "cvs.com",
        "walgreens.com",
        "target.com",
        "walmart.com",
        "beautylish.com",
        "dermstore.com",
        "nordstrom.com"
    ]
    
    return {"supported_websites": supported_sites}