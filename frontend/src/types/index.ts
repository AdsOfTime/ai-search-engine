export interface Product {
  id: number;
  name: string;
  description: string;
  category: string;
  subcategory?: string;
  brand: string;
  price: number;
  original_price?: number;
  discount_percentage?: number;
  rating: number;
  review_count: number;
  image_url: string;
  product_url: string;
  source_website: string;
  in_stock: boolean;
  features?: Record<string, any>;
  created_at: string;
  updated_at?: string;
}

export interface Review {
  id: number;
  product_id: number;
  reviewer_name?: string;
  rating: number;
  review_text: string;
  sentiment_score?: number;
  helpful_votes: number;
  verified_purchase: boolean;
  review_date: string;
  source_website: string;
  created_at: string;
}

export interface SearchFilters {
  category?: string;
  min_price?: number;
  max_price?: number;
  min_rating?: number;
  brand?: string;
  in_stock?: boolean;
}

export interface SearchParams extends SearchFilters {
  q: string;
  sort_by?: 'relevance' | 'price_low' | 'price_high' | 'rating';
  page?: number;
  limit?: number;
}

export interface SearchResults {
  products: Product[];
  total: number;
  page: number;
  limit: number;
  pages: number;
}

export interface PriceHistory {
  id: number;
  product_id: number;
  price: number;
  recorded_at: string;
}

export interface ApiError {
  message: string;
  details?: string;
}