import React from 'react';

interface RevenueData {
  total_monthly_revenue: number;
  annual_projection: number;
  revenue_per_click: number;
  affiliate_performance: Array<{
    retailer: string;
    clicks: number;
    estimated_revenue: number;
  }>;
  top_products: Array<{
    name: string;
    brand: string;
    clicks: number;
    revenue: number;
  }>;
}

const RevenueDashboard: React.FC = () => {
  const [revenueData, setRevenueData] = React.useState<RevenueData | null>(null);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    const fetchRevenueData = async () => {
      try {
        const response = await fetch('https://ai-search-backend.dnash29.workers.dev/api/analytics/revenue');
        const data = await response.json();
        setRevenueData(data);
      } catch (error) {
        console.error('Failed to fetch revenue data:', error);
      }
      setLoading(false);
    };

    fetchRevenueData();
  }, []);

  if (loading) {
    return (
      <div style={{ padding: '2rem', textAlign: 'center' }}>
        <div style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>📊</div>
        <div>Loading revenue analytics...</div>
      </div>
    );
  }

  if (!revenueData) {
    return (
      <div style={{ padding: '2rem', textAlign: 'center', color: '#ef4444' }}>
        Failed to load revenue data
      </div>
    );
  }

  return (
    <div style={{ 
      padding: '2rem',
      backgroundColor: '#f8fafc',
      borderRadius: '12px',
      margin: '2rem',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
    }}>
      <h2 style={{ 
        fontSize: '1.5rem',
        fontWeight: 'bold',
        marginBottom: '2rem',
        color: '#1f2937',
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem'
      }}>
        💰 Revenue Dashboard
      </h2>

      {/* Key Metrics */}
      <div style={{ 
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '1rem',
        marginBottom: '2rem'
      }}>
        <div style={{
          backgroundColor: 'white',
          padding: '1.5rem',
          borderRadius: '8px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#059669' }}>
            ${revenueData.revenue_projections?.monthly_projection?.toFixed(2) || '0.00'}
          </div>
          <div style={{ color: '#6b7280', fontSize: '0.875rem' }}>Monthly Revenue</div>
        </div>

        <div style={{
          backgroundColor: 'white',
          padding: '1.5rem',
          borderRadius: '8px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#dc2626' }}>
            ${revenueData.revenue_projections?.annual_projection?.toFixed(0) || '0'}
          </div>
          <div style={{ color: '#6b7280', fontSize: '0.875rem' }}>Annual Projection</div>
        </div>

        <div style={{
          backgroundColor: 'white',
          padding: '1.5rem',
          borderRadius: '8px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#7c3aed' }}>
            ${revenueData.revenue_projections?.revenue_per_click?.toFixed(3) || '0.000'}
          </div>
          <div style={{ color: '#6b7280', fontSize: '0.875rem' }}>Revenue per Click</div>
        </div>
      </div>

      {/* Affiliate Performance */}
      <div style={{ marginBottom: '2rem' }}>
        <h3 style={{ 
          fontSize: '1.25rem',
          fontWeight: 'semibold',
          marginBottom: '1rem',
          color: '#1f2937'
        }}>
          🔗 Affiliate Performance (Last 30 Days)
        </h3>
        <div style={{ backgroundColor: 'white', borderRadius: '8px', overflow: 'hidden' }}>
          {revenueData.affiliate_performance?.length ? (
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead style={{ backgroundColor: '#f3f4f6' }}>
                <tr>
                  <th style={{ padding: '0.75rem', textAlign: 'left', fontSize: '0.875rem', fontWeight: 'medium' }}>
                    Retailer
                  </th>
                  <th style={{ padding: '0.75rem', textAlign: 'right', fontSize: '0.875rem', fontWeight: 'medium' }}>
                    Clicks
                  </th>
                  <th style={{ padding: '0.75rem', textAlign: 'right', fontSize: '0.875rem', fontWeight: 'medium' }}>
                    Est. Revenue
                  </th>
                </tr>
              </thead>
              <tbody>
                {revenueData.affiliate_performance.map((item, index) => (
                  <tr key={index} style={{ borderTop: index > 0 ? '1px solid #e5e7eb' : 'none' }}>
                    <td style={{ padding: '0.75rem', fontSize: '0.875rem', fontWeight: 'medium' }}>
                      {item.retailer}
                    </td>
                    <td style={{ padding: '0.75rem', textAlign: 'right', fontSize: '0.875rem' }}>
                      {item.clicks}
                    </td>
                    <td style={{ padding: '0.75rem', textAlign: 'right', fontSize: '0.875rem', color: '#059669' }}>
                      ${item.estimated_revenue.toFixed(2)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div style={{ padding: '2rem', textAlign: 'center', color: '#6b7280' }}>
              No affiliate data yet. Start promoting products to see revenue!
            </div>
          )}
        </div>
      </div>

      {/* Top Products */}
      <div>
        <h3 style={{ 
          fontSize: '1.25rem',
          fontWeight: 'semibold',
          marginBottom: '1rem',
          color: '#1f2937'
        }}>
          🏆 Top Revenue Products
        </h3>
        <div style={{ backgroundColor: 'white', borderRadius: '8px', overflow: 'hidden' }}>
          {revenueData.top_products?.length ? (
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead style={{ backgroundColor: '#f3f4f6' }}>
                <tr>
                  <th style={{ padding: '0.75rem', textAlign: 'left', fontSize: '0.875rem', fontWeight: 'medium' }}>
                    Product
                  </th>
                  <th style={{ padding: '0.75rem', textAlign: 'right', fontSize: '0.875rem', fontWeight: 'medium' }}>
                    Clicks
                  </th>
                  <th style={{ padding: '0.75rem', textAlign: 'right', fontSize: '0.875rem', fontWeight: 'medium' }}>
                    Revenue
                  </th>
                </tr>
              </thead>
              <tbody>
                {revenueData.top_products.slice(0, 10).map((product, index) => (
                  <tr key={index} style={{ borderTop: index > 0 ? '1px solid #e5e7eb' : 'none' }}>
                    <td style={{ padding: '0.75rem', fontSize: '0.875rem' }}>
                      <div style={{ fontWeight: 'medium' }}>{product.name}</div>
                      <div style={{ fontSize: '0.75rem', color: '#6b7280' }}>{product.brand}</div>
                    </td>
                    <td style={{ padding: '0.75rem', textAlign: 'right', fontSize: '0.875rem' }}>
                      {product.clicks}
                    </td>
                    <td style={{ padding: '0.75rem', textAlign: 'right', fontSize: '0.875rem', color: '#059669' }}>
                      ${product.revenue.toFixed(2)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div style={{ padding: '2rem', textAlign: 'center', color: '#6b7280' }}>
              No product revenue data yet. Products will appear here once users start clicking!
            </div>
          )}
        </div>
      </div>

      <div style={{ 
        marginTop: '2rem',
        padding: '1rem',
        backgroundColor: '#dbeafe',
        borderRadius: '8px',
        fontSize: '0.875rem',
        color: '#1e40af'
      }}>
        💡 <strong>Monetization Tip:</strong> Revenue grows with traffic! Focus on SEO, social media, and content marketing to increase visitors and affiliate commissions.
      </div>
    </div>
  );
};

export default RevenueDashboard;