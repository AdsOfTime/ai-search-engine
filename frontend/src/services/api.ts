import axios from 'axios';
import { SearchParams, SearchResults, Product, Review, PriceHistory } from '../types';

// Cloudflare Worker API URL - now using your deployed worker
const getApiUrl = () => {
  // Check if we have a custom API URL from environment
  if (window?.location?.hostname?.includes('.pages.dev')) {
    // Running on Cloudflare Pages, use worker API
    return 'https://ai-search-backend.dnash29.workers.dev/api';
  }
  
  // Development or local environment - you can switch between local and live API
  return 'https://ai-search-backend.dnash29.workers.dev/api'; // Using live API
  // return 'http://localhost:8002/api'; // Uncomment for local development
};

const API_BASE_URL = getApiUrl();

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// Add request interceptor for auth tokens
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const searchAPI = {
  searchProducts: async (params: SearchParams): Promise<SearchResults> => {
    const response = await apiClient.get('/search/products', { params });
    return response.data;
  },

  getSuggestions: async (query: string): Promise<string[]> => {
    const response = await apiClient.get('/search/suggestions', {
      params: { q: query }
    });
    return response.data.suggestions;
  },

  getTrendingProducts: async (category?: string, limit: number = 10): Promise<Product[]> => {
    const response = await apiClient.get('/search/trending', {
      params: { category, limit }
    });
    return response.data.trending_products;
  }
};

export const productAPI = {
  getProduct: async (productId: number): Promise<{ product: Product; reviews: Review[] }> => {
    const response = await apiClient.get(`/products/${productId}`);
    return response.data;
  },

  getProductReviews: async (
    productId: number, 
    page: number = 1, 
    limit: number = 20
  ): Promise<{ reviews: Review[]; total: number; page: number; limit: number }> => {
    const response = await apiClient.get(`/products/${productId}/reviews`, {
      params: { page, limit }
    });
    return response.data;
  },

  getPriceHistory: async (productId: number): Promise<PriceHistory[]> => {
    const response = await apiClient.get(`/products/${productId}/price-history`);
    return response.data.price_history;
  },

  getSimilarProducts: async (productId: number, limit: number = 10): Promise<Product[]> => {
    const response = await apiClient.get(`/products/${productId}/similar`, {
      params: { limit }
    });
    return response.data.similar_products;
  }
};

export const scraperAPI = {
  getSupportedWebsites: async (): Promise<string[]> => {
    const response = await apiClient.get('/scraper/supported-websites');
    return response.data.supported_websites;
  },

  startScraping: async (websites: string[], categories: string[]): Promise<any> => {
    const response = await apiClient.post('/scraper/start-scraping', {
      websites,
      categories
    });
    return response.data;
  },

  getScrapingStatus: async (): Promise<any> => {
    const response = await apiClient.get('/scraper/scraping-status');
    return response.data;
  }
};

export default apiClient;