#!/usr/bin/env python3
"""
Affiliate Marketing Service
Generate affiliate links and track commissions
"""

import hashlib
import uuid
from typing import Dict, Optional
from urllib.parse import urlencode

class AffiliateService:
    def __init__(self):
        self.affiliate_programs = {
            "amazon": {
                "tag": "yourtag-20",
                "base_url": "https://www.amazon.com/dp/",
                "commission_rate": 0.04  # 4%
            },
            "sephora": {
                "tag": "your_sephora_id",
                "base_url": "https://www.sephora.com/",
                "commission_rate": 0.05  # 5%
            },
            "ulta": {
                "tag": "your_ulta_id", 
                "base_url": "https://www.ulta.com/",
                "commission_rate": 0.06  # 6%
            },
            "nike": {
                "tag": "your_nike_id",
                "base_url": "https://www.nike.com/",
                "commission_rate": 0.03  # 3%
            },
            "cvs": {
                "tag": "your_cvs_id",
                "base_url": "https://www.cvs.com/",
                "commission_rate": 0.04  # 4%
            }
        }
    
    def generate_affiliate_link(self, product_id: str, retailer: str, original_url: str) -> str:
        """Generate tracked affiliate link"""
        if retailer not in self.affiliate_programs:
            return original_url
        
        affiliate_info = self.affiliate_programs[retailer]
        
        # Create tracking parameters
        tracking_id = str(uuid.uuid4())[:8]
        params = {
            "tag": affiliate_info["tag"],
            "ref": f"ai_search_{tracking_id}",
            "linkCode": "ur2",
            "camp": "1789",
            "creative": "9325"
        }
        
        # Build affiliate URL
        if "amazon" in retailer:
            return f"{affiliate_info['base_url']}{product_id}?{urlencode(params)}"
        else:
            return f"{original_url}?{urlencode(params)}"
    
    def calculate_commission(self, sale_amount: float, retailer: str) -> float:
        """Calculate expected commission"""
        if retailer in self.affiliate_programs:
            rate = self.affiliate_programs[retailer]["commission_rate"]
            return sale_amount * rate
        return 0.0
    
    def get_retailer_info(self) -> Dict:
        """Get all retailer commission rates"""
        return {
            retailer: {
                "commission_rate": info["commission_rate"],
                "rate_percentage": f"{info['commission_rate']*100}%"
            }
            for retailer, info in self.affiliate_programs.items()
        }

# Revenue estimation for different monetization models
class RevenueCalculator:
    def __init__(self):
        self.models = {
            "affiliate": {
                "avg_commission_per_sale": 2.50,
                "conversion_rate": 0.02,  # 2%
                "description": "Commission from product sales"
            },
            "advertising": {
                "cpm": 5.00,  # $5 per 1000 impressions
                "ctr": 0.015,  # 1.5% click rate
                "cpc": 0.75,   # $0.75 per click
                "description": "Display ads and sponsored products"
            },
            "premium_features": {
                "monthly_subscription": 9.99,
                "conversion_rate": 0.05,  # 5% of users go premium
                "description": "Premium search features, alerts, comparisons"
            },
            "api_access": {
                "per_request": 0.001,  # $0.001 per API call
                "enterprise_monthly": 299,
                "description": "API access for other businesses"
            },
            "sponsored_listings": {
                "per_listing_monthly": 49.99,
                "featured_placement": 99.99,
                "description": "Retailers pay for prominent placement"
            }
        }
    
    def estimate_monthly_revenue(self, monthly_visitors: int, user_engagement: dict = None) -> Dict:
        """Estimate revenue based on traffic"""
        if not user_engagement:
            user_engagement = {
                "avg_searches_per_visit": 3,
                "avg_products_viewed": 8,
                "click_through_rate": 0.15
            }
        
        revenue_breakdown = {}
        
        # Affiliate Marketing
        monthly_clicks = monthly_visitors * user_engagement["click_through_rate"]
        affiliate_sales = monthly_clicks * self.models["affiliate"]["conversion_rate"]
        affiliate_revenue = affiliate_sales * self.models["affiliate"]["avg_commission_per_sale"]
        revenue_breakdown["affiliate"] = {
            "revenue": affiliate_revenue,
            "details": f"{affiliate_sales:.0f} sales × ${self.models['affiliate']['avg_commission_per_sale']}"
        }
        
        # Advertising
        monthly_pageviews = monthly_visitors * user_engagement["avg_products_viewed"]
        ad_impressions = monthly_pageviews * 2  # 2 ads per page
        ad_clicks = ad_impressions * self.models["advertising"]["ctr"]
        ad_revenue = (ad_impressions / 1000 * self.models["advertising"]["cpm"]) + \
                    (ad_clicks * self.models["advertising"]["cpc"])
        revenue_breakdown["advertising"] = {
            "revenue": ad_revenue,
            "details": f"{ad_impressions/1000:.0f}k impressions + {ad_clicks:.0f} clicks"
        }
        
        # Premium Subscriptions
        premium_users = monthly_visitors * self.models["premium_features"]["conversion_rate"]
        premium_revenue = premium_users * self.models["premium_features"]["monthly_subscription"]
        revenue_breakdown["premium"] = {
            "revenue": premium_revenue,
            "details": f"{premium_users:.0f} users × ${self.models['premium_features']['monthly_subscription']}"
        }
        
        # Calculate total
        total_revenue = sum(item["revenue"] for item in revenue_breakdown.values())
        
        return {
            "monthly_visitors": monthly_visitors,
            "total_monthly_revenue": total_revenue,
            "annual_projection": total_revenue * 12,
            "breakdown": revenue_breakdown,
            "revenue_per_visitor": total_revenue / monthly_visitors if monthly_visitors > 0 else 0
        }

# Example usage
if __name__ == "__main__":
    # Test affiliate service
    affiliate = AffiliateService()
    print("Affiliate Programs:")
    for retailer, info in affiliate.get_retailer_info().items():
        print(f"- {retailer.title()}: {info['rate_percentage']} commission")
    
    # Test revenue calculator
    calculator = RevenueCalculator()
    
    # Different traffic scenarios
    scenarios = [
        {"name": "Launch (1K visitors/month)", "visitors": 1000},
        {"name": "Growth (10K visitors/month)", "visitors": 10000}, 
        {"name": "Scale (50K visitors/month)", "visitors": 50000},
        {"name": "Success (100K visitors/month)", "visitors": 100000}
    ]
    
    print("\n" + "="*60)
    print("REVENUE PROJECTIONS")
    print("="*60)
    
    for scenario in scenarios:
        result = calculator.estimate_monthly_revenue(scenario["visitors"])
        print(f"\n{scenario['name']}:")
        print(f"  Monthly Revenue: ${result['total_monthly_revenue']:,.2f}")
        print(f"  Annual Projection: ${result['annual_projection']:,.2f}")
        print(f"  Revenue per Visitor: ${result['revenue_per_visitor']:.2f}")
        print("  Breakdown:")
        for source, data in result["breakdown"].items():
            print(f"    - {source.title()}: ${data['revenue']:,.2f} ({data['details']})")