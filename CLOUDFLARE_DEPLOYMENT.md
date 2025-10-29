# Environment Configuration for Cloudflare Deployment

## Required Environment Variables

### 1. Cloudflare Worker Secrets
Set these using `wrangler secret put <SECRET_NAME>`:

```bash
# OpenAI API Key for AI features
wrangler secret put OPENAI_API_KEY

# Database connection (if using external database)
wrangler secret put DATABASE_URL

# Application secret key for security
wrangler secret put SECRET_KEY

# Affiliate program API keys (optional)
wrangler secret put AMAZON_AFFILIATE_KEY
wrangler secret put SEPHORA_AFFILIATE_KEY
```

### 2. Frontend Environment Variables
Create `.env.production` in the frontend directory:

```bash
# Cloudflare Worker API URL (update with your actual worker URL)
REACT_APP_API_URL=https://your-worker.your-subdomain.workers.dev/api

# Enable production features
REACT_APP_ENVIRONMENT=production

# Analytics and tracking (optional)
REACT_APP_GOOGLE_ANALYTICS_ID=your-ga-id
REACT_APP_SENTRY_DSN=your-sentry-dsn
```

### 3. Wrangler Configuration
Update `wrangler.toml` with your actual values:

```toml
# Replace with your actual domain
[[routes]]
pattern = "yourdomain.com/api/*"
zone_name = "yourdomain.com"

# Replace with your actual D1 database ID
[[env.production.d1_databases]]
binding = "DB"
database_name = "ai-search-db"
database_id = "your-actual-d1-database-id"

# Replace with your actual KV namespace ID
[[env.production.kv_namespaces]]
binding = "CACHE"
id = "your-actual-kv-namespace-id"
```

### 4. Cloudflare Pages Configuration
In your Cloudflare Pages dashboard, set:

- **Build command**: `npm run build`
- **Build output directory**: `build`
- **Root directory**: `frontend`
- **Node.js version**: `18`

### 5. Database Configuration Options

#### Option A: Cloudflare D1 (Recommended)
- Fully managed SQL database
- Integrated with Workers
- Global edge locations
- Automatic scaling

#### Option B: External Database
Set `DATABASE_URL` secret for:
- PostgreSQL
- MySQL
- PlanetScale
- Supabase

## Deployment Commands

### Quick Deploy (PowerShell on Windows):
```powershell
# Full deployment
.\deploy-cloudflare.ps1 -DeploymentType full

# Backend only
.\deploy-cloudflare.ps1 -DeploymentType backend

# Frontend only
.\deploy-cloudflare.ps1 -DeploymentType frontend
```

### Manual Deployment Steps:

1. **Install Wrangler CLI**:
```bash
npm install -g wrangler
```

2. **Login to Cloudflare**:
```bash
wrangler login
```

3. **Create D1 Database**:
```bash
wrangler d1 create ai-search-db
```

4. **Apply Database Schema**:
```bash
wrangler d1 execute ai-search-db --file=cloudflare-d1-schema.sql
```

5. **Deploy Worker**:
```bash
cd cloudflare-workers
npm install
wrangler publish
```

6. **Deploy Frontend to Pages**:
- Connect GitHub repository to Cloudflare Pages
- Set build configuration
- Deploy automatically on git push

## Performance Optimization

### 1. Caching Strategy
- **KV Store**: Cache search results for 5 minutes
- **Browser Cache**: Static assets cached for 1 year
- **CDN**: Cloudflare's global CDN for fast delivery

### 2. Database Optimization
- **Indexes**: Created on frequently queried columns
- **Pagination**: Limit results to prevent large responses
- **Connection Pooling**: Managed by Cloudflare D1

### 3. AI Model Optimization
- **Model Loading**: Lazy load AI models when needed
- **Batch Processing**: Process multiple items together
- **Caching**: Cache AI results to reduce API calls

## Security Configuration

### 1. CORS Settings
Configure allowed origins in Worker:
```typescript
cors({
  origin: ['https://yourdomain.com', 'https://*.pages.dev'],
  allowHeaders: ['Content-Type', 'Authorization'],
  allowMethods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
})
```

### 2. Rate Limiting
Implement rate limiting to prevent abuse:
- Search API: 100 requests/minute per IP
- Scraper API: 10 requests/minute per IP
- Product API: 200 requests/minute per IP

### 3. Input Validation
- Sanitize all user inputs
- Validate query parameters
- Prevent SQL injection with parameterized queries

## Monitoring and Logging

### 1. Cloudflare Analytics
- Real-time traffic analytics
- Performance metrics
- Error tracking

### 2. Worker Logs
Monitor worker performance:
```bash
wrangler tail
```

### 3. Database Monitoring
- Query performance metrics
- Storage usage tracking
- Connection monitoring

## Cost Optimization

### Free Tier Limits:
- **Workers**: 100,000 requests/day
- **D1**: 5GB storage, 25M row reads/month
- **KV**: 1GB storage, 10M reads/month
- **Pages**: 1 build/minute, 500 builds/month

### Paid Plans:
- **Workers Paid**: $5/month + usage
- **D1**: $0.001 per 1K reads after free tier
- **KV**: $0.50 per GB/month after free tier

## Troubleshooting

### Common Issues:

1. **Worker Deploy Fails**:
   - Check wrangler.toml configuration
   - Verify authentication with `wrangler whoami`
   - Ensure all required secrets are set

2. **Database Connection Issues**:
   - Verify D1 database ID in wrangler.toml
   - Check database schema is applied
   - Ensure proper binding name (DB)

3. **Frontend API Calls Fail**:
   - Update API_BASE_URL with actual worker URL
   - Check CORS configuration
   - Verify worker is deployed and accessible

4. **AI Features Not Working**:
   - Ensure OPENAI_API_KEY secret is set
   - Check API quota limits
   - Verify model names are correct

## Support Resources

- **Cloudflare Docs**: https://developers.cloudflare.com
- **Workers Documentation**: https://developers.cloudflare.com/workers
- **D1 Documentation**: https://developers.cloudflare.com/d1
- **Pages Documentation**: https://developers.cloudflare.com/pages
- **Community Discord**: https://discord.cloudflare.com