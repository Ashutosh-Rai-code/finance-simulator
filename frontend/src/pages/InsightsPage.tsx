import { useEffect, useState, useRef } from 'react';
import './InsightsPage.css';
import { visitorService } from '../services/api';

function InsightsPage() {
  const [visitorCount, setVisitorCount] = useState<number | null>(null);
  const [visitorError, setVisitorError] = useState<string | null>(null);
  const hasTrackedRef = useRef(false);

  useEffect(() => {
    const trackVisitor = async () => {
      // Only track once per session
      if (hasTrackedRef.current) {
        return;
      }
      
      hasTrackedRef.current = true;
      
      try {
        const response = await visitorService.incrementVisitorCount();
        setVisitorCount(response.data.count);
      } catch (error) {
        console.error('Visitor counter error:', error);
        setVisitorError('Unable to load live visitor count.');
      }
    };

    trackVisitor();
  }, []);

  return (
    <div className="insights-page">
      <div className="insights-header">
        <h2>📊 Financial Insights</h2>
        <p>Quick overview of your money health and opportunity areas.</p>
      </div>

      <div className="insights-grid">
        <div className="insights-card">
          <h3>Top Insight</h3>
          <p>Emergency fund coverage is low — target 6-12 months of expenses.</p>
        </div>

        <div className="insights-card">
          <h3>Actionable Opportunity</h3>
          <p>Increase SIP by at least 15% to improve long-term wealth by ₹30L in 5 years.</p>
        </div>

        <div className="insights-card">
          <h3>Risk Watch</h3>
          <p>Monthly expenses are above 50% of income — reduce discretionary spending.</p>
        </div>
      </div>

      <div className="visitor-counter">
        <p className="visitor-text">
          🌍 Unique visitors: <strong>{visitorCount !== null ? visitorCount : 'Loading...'}</strong>
        </p>
        {visitorError && <p className="visitor-error">{visitorError}</p>}
      </div>
    </div>
  );
}

export default InsightsPage;
