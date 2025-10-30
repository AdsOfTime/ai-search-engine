import { Hono } from 'hono'
import { cors } from 'hono/cors'
import { bearerAuth } from 'hono/bearer-auth'

// Types for our AI Search Engine
interface Product {
  id: string
  name: string
  brand: string
  category: string
  price: number
  rating: number
  review_count: number
  description: string
  image_url?: string
  in_stock: boolean
  affiliate_links?: Record<string, string>
  commission_rate?: number
  featured_placement?: boolean
}

interface AffiliateClick {
  id: string
  product_id: string
  user_id?: string
  retailer: string
  timestamp: string
  revenue_potential: number
}

interface SearchQuery {
  q: string
  category?: string
  min_price?: number
  max_price?: number
  brand?: string
  sort_by?: string
  limit?: number
  offset?: number
}

interface AISearchResponse {
  products: Product[]
  total: number
  ai_enhanced_query?: string
  search_intent?: any
  recommendations?: any[]
}

// Initialize Hono app
const app = new Hono<{
  Bindings: {
    DB: D1Database
    CACHE: KVNamespace
    MEDIA: R2Bucket
    OPENAI_API_KEY: string
    DATABASE_URL: string
    SECRET_KEY: string
  }
}>()

// CORS middleware
app.use('*', cors({
  origin: ['https://ai-search-engine-1hh.pages.dev', 'https://*.pages.dev', 'http://localhost:3000'],
  allowHeaders: ['Content-Type', 'Authorization'],
  allowMethods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
}))

// Health check endpoint
app.get('/api/health', async (c) => {
  return c.json({ 
    status: 'healthy',
    timestamp: new Date().toISOString(),
    version: '1.0.0'
  })
})

// AI-powered product search endpoint
app.get('/api/search/products', async (c) => {
  try {
    const query: SearchQuery = {
      q: c.req.query('q') || '',
      category: c.req.query('category'),
      min_price: c.req.query('min_price') ? parseFloat(c.req.query('min_price')!) : undefined,
      max_price: c.req.query('max_price') ? parseFloat(c.req.query('max_price')!) : undefined,
      brand: c.req.query('brand'),
      sort_by: c.req.query('sort_by') || 'relevance',
      limit: c.req.query('limit') ? parseInt(c.req.query('limit')!) : 20,
      offset: c.req.query('offset') ? parseInt(c.req.query('offset')!) : 0
    }

    // Check cache first
    const cacheKey = `search:${JSON.stringify(query)}`
    const cached = await c.env.CACHE.get(cacheKey, 'json')
    
    if (cached) {
      return c.json(cached)
    }

    // Build SQL query with search terms
    let sql = `
      SELECT 
        id, name, brand, category, price, rating, review_count, 
        description, image_url, in_stock, affiliate_links
      FROM products 
      WHERE in_stock = 1
    `
    const params: any[] = []

    // Add search conditions - prioritize basic search first
    if (query.q && query.q.length > 0) {
      sql += ` AND (name LIKE ? OR description LIKE ? OR brand LIKE ? OR category LIKE ?)`
      const searchTerm = `%${query.q}%`
      params.push(searchTerm, searchTerm, searchTerm, searchTerm)
    }
    
    // AI Enhancement: Try to enhance search query using OpenAI (async, won't block search)
    let enhancedQuery = ''
    try {
      if (query.q && c.env.OPENAI_API_KEY) {
        enhancedQuery = await enhanceSearchQuery(query.q, c.env.OPENAI_API_KEY)
      }
    } catch (error) {
      // AI enhancement failed, continue with basic search
      console.log('AI enhancement failed:', error)
    }

    if (query.category) {
      sql += ` AND category = ?`
      params.push(query.category)
    }

    if (query.brand) {
      sql += ` AND brand = ?`
      params.push(query.brand)
    }

    if (query.min_price !== undefined) {
      sql += ` AND price >= ?`
      params.push(query.min_price)
    }

    if (query.max_price !== undefined) {
      sql += ` AND price <= ?`
      params.push(query.max_price)
    }

    // AI Ranking: Sort by AI-calculated relevance score
    switch (query.sort_by) {
      case 'price_asc':
        sql += ` ORDER BY price ASC`
        break
      case 'price_desc':
        sql += ` ORDER BY price DESC`
        break
      case 'rating':
        sql += ` ORDER BY rating DESC, review_count DESC`
        break
      case 'popularity':
        sql += ` ORDER BY review_count DESC, rating DESC`
        break
      default: // AI relevance
        sql += ` ORDER BY (rating * 0.3 + (review_count / 100.0) * 0.2 + 
                          CASE WHEN name LIKE ? THEN 0.5 ELSE 0 END) DESC`
        params.push(`%${query.q}%`)
    }

    sql += ` LIMIT ? OFFSET ?`
    params.push(query.limit!, query.offset!)

    // Execute database query
    const results = await c.env.DB.prepare(sql).bind(...params).all()
    
    // Get total count for pagination
    let countSql = `SELECT COUNT(*) as total FROM products WHERE in_stock = 1`
    const countParams: any[] = []
    
    if (enhancedQuery) {
      countSql += ` AND (name LIKE ? OR description LIKE ? OR brand LIKE ?)`
      const searchTerm = `%${enhancedQuery}%`
      countParams.push(searchTerm, searchTerm, searchTerm)
    }
    
    const totalResult = await c.env.DB.prepare(countSql).bind(...countParams).first()
    const total = totalResult?.total || 0

    // AI Analysis: Analyze search intent
    const searchIntent = analyzeSearchIntent(query.q)

    // AI Recommendations: Generate smart recommendations
    const recommendations = await generateRecommendations(results.results as Product[], c.env.DB)

    const response: AISearchResponse = {
      products: results.results as Product[],
      total: total as number,
      ai_enhanced_query: enhancedQuery,
      search_intent: searchIntent,
      recommendations: recommendations
    }

    // Cache results for 5 minutes
    await c.env.CACHE.put(cacheKey, JSON.stringify(response), { expirationTtl: 300 })

    return c.json(response)

  } catch (error) {
    console.error('Search error:', error)
    return c.json({ error: 'Search failed' }, 500)
  }
})

// AI-powered product details with sentiment analysis
app.get('/api/products/:id', async (c) => {
  try {
    const productId = c.req.param('id')
    
    // Get product details
    const product = await c.env.DB.prepare(`
      SELECT * FROM products WHERE id = ?
    `).bind(productId).first()

    if (!product) {
      return c.json({ error: 'Product not found' }, 404)
    }

    // Get reviews
    const reviews = await c.env.DB.prepare(`
      SELECT review_text, rating, created_at 
      FROM reviews 
      WHERE product_id = ? 
      ORDER BY created_at DESC 
      LIMIT 50
    `).bind(productId).all()

    // AI Sentiment Analysis
    const sentimentAnalysis = await analyzeSentiment(
      reviews.results.map((r: any) => r.review_text),
      c.env.OPENAI_API_KEY
    )

    // AI Similar Products
    const similarProducts = await findSimilarProducts(product as Product, c.env.DB)

    return c.json({
      product,
      reviews: reviews.results,
      sentiment_analysis: sentimentAnalysis,
      similar_products: similarProducts,
      ai_insights: {
        overall_sentiment: sentimentAnalysis.overall_sentiment,
        recommendation_strength: sentimentAnalysis.overall_sentiment > 0.5 ? 'highly_recommended' : 'moderately_recommended'
      }
    })

  } catch (error) {
    console.error('Product details error:', error)
    return c.json({ error: 'Failed to get product details' }, 500)
  }
})

// AI product recommendations endpoint
app.get('/api/recommendations/:userId?', async (c) => {
  try {
    const userId = c.req.param('userId')
    
    let recommendations: Product[] = []
    
    if (userId) {
      // Personalized recommendations based on user history
      const userHistory = await c.env.DB.prepare(`
        SELECT p.* FROM products p
        JOIN user_interactions ui ON p.id = ui.product_id
        WHERE ui.user_id = ?
        ORDER BY ui.created_at DESC
        LIMIT 10
      `).bind(userId).all()
      
      recommendations = await generatePersonalizedRecommendations(
        userHistory.results as Product[], 
        c.env.DB
      )
    } else {
      // General trending recommendations
      recommendations = await getTrendingProducts(c.env.DB)
    }

    return c.json({
      recommendations,
      recommendation_type: userId ? 'personalized' : 'trending',
      ai_powered: true
    })

  } catch (error) {
    console.error('Recommendations error:', error)
    return c.json({ error: 'Failed to get recommendations' }, 500)
  }
})

// 💰 MONETIZATION ENDPOINTS

// Track affiliate clicks and generate revenue
app.post('/api/affiliate/click', async (c) => {
  try {
    const { product_id, retailer, user_id } = await c.req.json()
    
    // Generate affiliate link and tracking
    const affiliateData = generateAffiliateLink(product_id, retailer)
    
    // Store click for analytics
    const clickId = crypto.randomUUID()
    await c.env.DB.prepare(`
      INSERT INTO affiliate_clicks (id, product_id, user_id, retailer, timestamp, revenue_potential)
      VALUES (?, ?, ?, ?, ?, ?)
    `).bind(
      clickId,
      product_id,
      user_id || null,
      retailer,
      new Date().toISOString(),
      affiliateData.commission_estimate
    ).run()

    return c.json({
      click_id: clickId,
      affiliate_url: affiliateData.url,
      commission_rate: affiliateData.commission_rate,
      tracking_enabled: true
    })

  } catch (error) {
    console.error('Affiliate click error:', error)
    return c.json({ error: 'Failed to track click' }, 500)
  }
})

// Revenue analytics dashboard
app.get('/api/analytics/revenue', async (c) => {
  try {
    // Get affiliate performance
    const affiliateStats = await c.env.DB.prepare(`
      SELECT 
        retailer,
        COUNT(*) as clicks,
        SUM(revenue_potential) as estimated_revenue,
        DATE(timestamp) as date
      FROM affiliate_clicks 
      WHERE timestamp > datetime('now', '-30 days')
      GROUP BY retailer, DATE(timestamp)
      ORDER BY estimated_revenue DESC
    `).all()

    // Get top performing products
    const topProducts = await c.env.DB.prepare(`
      SELECT 
        p.name, p.brand, p.category, p.price,
        COUNT(ac.id) as clicks,
        SUM(ac.revenue_potential) as revenue
      FROM products p
      JOIN affiliate_clicks ac ON p.id = ac.product_id
      WHERE ac.timestamp > datetime('now', '-30 days')
      GROUP BY p.id
      ORDER BY revenue DESC
      LIMIT 20
    `).all()

    // Calculate revenue projections
    const totalClicks = affiliateStats.results.reduce((sum: number, row: any) => sum + row.clicks, 0)
    const totalRevenue = affiliateStats.results.reduce((sum: number, row: any) => sum + row.estimated_revenue, 0)
    
    const projections = {
      daily_avg_clicks: totalClicks / 30,
      daily_avg_revenue: totalRevenue / 30,
      monthly_projection: totalRevenue,
      annual_projection: totalRevenue * 12,
      revenue_per_click: totalClicks > 0 ? totalRevenue / totalClicks : 0
    }

    return c.json({
      affiliate_performance: affiliateStats.results,
      top_products: topProducts.results,
      revenue_projections: projections,
      last_updated: new Date().toISOString()
    })

  } catch (error) {
    console.error('Revenue analytics error:', error)
    return c.json({ error: 'Failed to get analytics' }, 500)
  }
})

// Premium features endpoint (requires auth)
app.get('/api/premium/advanced-search', async (c) => {
  try {
    const authHeader = c.req.header('Authorization')
    if (!authHeader?.startsWith('Bearer ')) {
      return c.json({ error: 'Premium feature requires authentication' }, 401)
    }

    // Enhanced search with premium filters
    const query: SearchQuery = {
      q: c.req.query('q') || '',
      category: c.req.query('category'),
      min_price: c.req.query('min_price') ? parseFloat(c.req.query('min_price')!) : undefined,
      max_price: c.req.query('max_price') ? parseFloat(c.req.query('max_price')!) : undefined,
      brand: c.req.query('brand'),
      sort_by: c.req.query('sort_by') || 'relevance',
      limit: 50, // Premium users get more results
      offset: c.req.query('offset') ? parseInt(c.req.query('offset')!) : 0
    }

    // Premium-only filters
    const rating_min = c.req.query('rating_min') ? parseFloat(c.req.query('rating_min')!) : undefined
    const review_count_min = c.req.query('review_count_min') ? parseInt(c.req.query('review_count_min')!) : undefined
    const availability = c.req.query('availability') // in_stock, out_of_stock, all
    const discount_min = c.req.query('discount_min') ? parseFloat(c.req.query('discount_min')!) : undefined

    // Build enhanced SQL query
    let sql = `
      SELECT 
        id, name, brand, category, price, rating, review_count, 
        description, image_url, in_stock, affiliate_links
      FROM products 
      WHERE 1=1
    `
    const params: any[] = []

    if (query.q) {
      sql += ` AND (name LIKE ? OR description LIKE ? OR brand LIKE ?)`
      params.push(`%${query.q}%`, `%${query.q}%`, `%${query.q}%`)
    }

    if (rating_min) {
      sql += ` AND rating >= ?`
      params.push(rating_min)
    }

    if (review_count_min) {
      sql += ` AND review_count >= ?`
      params.push(review_count_min)
    }

    if (availability === 'in_stock') {
      sql += ` AND in_stock = 1`
    } else if (availability === 'out_of_stock') {
      sql += ` AND in_stock = 0`
    }

    sql += ` ORDER BY rating DESC, review_count DESC LIMIT ? OFFSET ?`
    params.push(query.limit, query.offset)

    const results = await c.env.DB.prepare(sql).bind(...params).all()

    return c.json({
      products: results.results,
      total: results.results.length,
      premium_features_used: {
        advanced_filters: true,
        enhanced_sorting: true,
        increased_results: true
      },
      query_analysis: await analyzeSearchIntent(query.q || '')
    })

  } catch (error) {
    console.error('Premium search error:', error)
    return c.json({ error: 'Premium search failed' }, 500)
  }
})

// Helper Functions for AI Features

// Monetization Helper Functions
function generateAffiliateLink(productId: string, retailer: string) {
  const affiliatePrograms = {
    amazon: { tag: 'aiprodsearch-20', commission: 0.04, base: 'https://www.amazon.com/dp/' },
    sephora: { tag: 'aisearch', commission: 0.05, base: 'https://www.sephora.com/' },
    target: { tag: 'aisearch', commission: 0.03, base: 'https://www.target.com/' },
    cvs: { tag: 'aisearch', commission: 0.04, base: 'https://www.cvs.com/' },
    ulta: { tag: 'aisearch', commission: 0.06, base: 'https://www.ulta.com/' }
  }

  const program = affiliatePrograms[retailer as keyof typeof affiliatePrograms]
  if (!program) {
    return {
      url: `https://example.com/products/${productId}`,
      commission_rate: 0,
      commission_estimate: 0
    }
  }

  // Generate tracking URL
  const trackingId = crypto.randomUUID().substring(0, 8)
  const affiliateUrl = `${program.base}${productId}?tag=${program.tag}&ref=aisearch_${trackingId}`
  
  // Estimate commission (average product price $25)
  const estimatedCommission = 25 * program.commission

  return {
    url: affiliateUrl,
    commission_rate: program.commission,
    commission_estimate: estimatedCommission
  }
}

async function enhanceSearchQuery(query: string, apiKey: string): Promise<string> {
  if (!query || !apiKey) return query

  try {
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: 'gpt-3.5-turbo',
        messages: [{
          role: 'system',
          content: 'You are an expert at enhancing e-commerce search queries. Add relevant synonyms and variations while keeping the original intent. Return only the enhanced query.'
        }, {
          role: 'user',
          content: `Enhance this product search query: "${query}"`
        }],
        max_tokens: 100,
        temperature: 0.3
      })
    })

    const data = await response.json()
    return data.choices[0]?.message?.content?.trim() || query
  } catch (error) {
    console.error('Query enhancement error:', error)
    return query
  }
}

function analyzeSearchIntent(query: string) {
  const lowerQuery = query.toLowerCase()
  
  const intents = {
    price_focused: /cheap|affordable|budget|deal|discount|sale/.test(lowerQuery),
    quality_focused: /best|top|premium|luxury|high-end/.test(lowerQuery),
    brand_specific: /brand|vs|compare/.test(lowerQuery),
    urgent: /urgent|fast|quick|immediate/.test(lowerQuery),
    gift: /gift|present|birthday/.test(lowerQuery)
  }
  
  const primaryIntent = Object.entries(intents).find(([_, match]) => match)?.[0] || 'general'
  
  return {
    primary_intent: primaryIntent,
    confidence: 0.8,
    extracted_entities: {
      price_indicators: lowerQuery.match(/\$?\d+/g) || [],
      brands: extractBrands(query),
      categories: extractCategories(query)
    }
  }
}

function extractBrands(query: string): string[] {
  const commonBrands = ['Fenty', 'Sephora', 'MAC', 'Maybelline', 'Nike', 'Adidas']
  return commonBrands.filter(brand => 
    query.toLowerCase().includes(brand.toLowerCase())
  )
}

function extractCategories(query: string): string[] {
  const categories = ['makeup', 'skincare', 'shoes', 'clothing', 'supplements']
  return categories.filter(cat => 
    query.toLowerCase().includes(cat)
  )
}

async function analyzeSentiment(reviews: string[], apiKey: string) {
  if (!reviews.length || !apiKey) {
    return { overall_sentiment: 0, confidence: 0 }
  }

  // Simple sentiment analysis for demo
  const positiveWords = ['good', 'great', 'excellent', 'amazing', 'love', 'perfect']
  const negativeWords = ['bad', 'terrible', 'awful', 'hate', 'worst', 'disappointing']
  
  let positiveCount = 0
  let negativeCount = 0
  
  reviews.forEach(review => {
    const lowerReview = review.toLowerCase()
    positiveCount += positiveWords.reduce((count, word) => 
      count + (lowerReview.split(word).length - 1), 0)
    negativeCount += negativeWords.reduce((count, word) => 
      count + (lowerReview.split(word).length - 1), 0)
  })
  
  const total = positiveCount + negativeCount
  const sentiment = total > 0 ? (positiveCount - negativeCount) / total : 0
  
  return {
    overall_sentiment: Math.max(-1, Math.min(1, sentiment)),
    confidence: Math.min(total / reviews.length, 1),
    positive_mentions: positiveCount,
    negative_mentions: negativeCount,
    reviews_analyzed: reviews.length
  }
}

async function findSimilarProducts(product: Product, db: D1Database): Promise<Product[]> {
  const results = await db.prepare(`
    SELECT * FROM products 
    WHERE category = ? 
      AND id != ? 
      AND in_stock = 1
      AND price BETWEEN ? AND ?
    ORDER BY rating DESC, review_count DESC
    LIMIT 6
  `).bind(
    product.category,
    product.id,
    product.price * 0.7,
    product.price * 1.3
  ).all()
  
  return results.results as Product[]
}

async function generateRecommendations(searchResults: Product[], db: D1Database): Promise<any[]> {
  if (!searchResults.length) return []
  
  const topCategory = searchResults[0]?.category
  
  const trending = await db.prepare(`
    SELECT * FROM products 
    WHERE category = ? 
      AND in_stock = 1 
    ORDER BY review_count DESC, rating DESC 
    LIMIT 3
  `).bind(topCategory).all()
  
  return (trending.results as Product[]).map(product => ({
    type: 'trending',
    product,
    reason: 'Popular in your search category'
  }))
}

async function generatePersonalizedRecommendations(userHistory: Product[], db: D1Database): Promise<Product[]> {
  if (!userHistory.length) return []
  
  const favoriteCategory = userHistory[0]?.category
  
  const results = await db.prepare(`
    SELECT * FROM products 
    WHERE category = ? 
      AND in_stock = 1 
    ORDER BY rating DESC 
    LIMIT 5
  `).bind(favoriteCategory).all()
  
  return results.results as Product[]
}

async function getTrendingProducts(db: D1Database): Promise<Product[]> {
  const results = await db.prepare(`
    SELECT * FROM products 
    WHERE in_stock = 1 
    ORDER BY review_count DESC, rating DESC 
    LIMIT 10
  `).all()
  
  return results.results as Product[]
}

export default app