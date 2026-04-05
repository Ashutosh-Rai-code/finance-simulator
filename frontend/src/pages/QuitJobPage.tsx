import { useState } from 'react';
import { LogOut, AlertCircle, CheckCircle } from 'lucide-react';
import { aiService } from '../services/api';
import './QuitJobPage.css';

function QuitJobPage() {
  const [savings, setSavings] = useState(500000);
  const [expenses, setExpenses] = useState(50000);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleAnalysis = async () => {
    setLoading(true);
    try {
      const response = await aiService.analyzeQuitJob(savings, expenses);
      setResult(response.data);
    } catch (error) {
      console.error('Analysis error:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (value: number) => {
    if (value >= 100000) return `₹${(value / 100000).toFixed(1)}L`;
    return `₹${value.toLocaleString()}`;
  };

  const months = savings / expenses;

  const getRiskColor = (risk: string) => {
    switch (risk.toLowerCase()) {
      case 'high':
        return 'high';
      case 'medium':
        return 'medium';
      case 'low':
      case 'safe':
        return 'low';
      default:
        return 'medium';
    }
  };

  return (
    <div className="quit-job-page">
      <div className="page-header">
        <h1 className="page-title">🚪 Quit Job Analysis</h1>
        <p className="page-subtitle">
          Evaluate if you're financially ready to leave your job
        </p>
      </div>

      <div className="analysis-container">
        <div className="input-section">
          <div className="input-group">
            <label>Total Savings</label>
            <input
              type="range"
              min={0}
              max={5000000}
              step={50000}
              value={savings}
              onChange={(e) => setSavings(parseInt(e.target.value))}
              className="input-slider"
            />
            <div className="input-value">{formatCurrency(savings)}</div>
          </div>

          <div className="input-group">
            <label>Monthly Expenses</label>
            <input
              type="range"
              min={5000}
              max={300000}
              step={5000}
              value={expenses}
              onChange={(e) => setExpenses(parseInt(e.target.value))}
              className="input-slider"
            />
            <div className="input-value">{formatCurrency(expenses)}</div>
          </div>

          <button className="analyze-btn" onClick={handleAnalysis} disabled={loading}>
            {loading ? 'Analyzing...' : 'Analyze'}
          </button>
        </div>

        <div className="metrics-section">
          <div className="metric-box">
            <p className="metric-label">Survival Months</p>
            <p className={`metric-value ${months < 6 ? 'danger' : months < 12 ? 'warning' : 'safe'}`}>
              {months.toFixed(1)}
            </p>
            <p className="metric-desc">
              {months < 6
                ? '⚠️ Too risky'
                : months < 12
                ? '⚠️ Limited runway'
                : '✅ Safe buffer'}
            </p>
          </div>

          <div className="metric-box">
            <p className="metric-label">Monthly Runway</p>
            <p className="metric-value">{formatCurrency(expenses)}</p>
            <p className="metric-desc">Your monthly expenses</p>
          </div>

          <div className="metric-box">
            <p className="metric-label">Total Runway</p>
            <p className="metric-value">{formatCurrency(savings - expenses)}</p>
            <p className="metric-desc">After one month</p>
          </div>
        </div>
      </div>

      {result && (
        <div className={`result-section ${getRiskColor(result.risk_level)}`}>
          <div className="result-header">
            {getRiskColor(result.risk_level) === 'low' ? (
              <CheckCircle size={32} className="result-icon safe" />
            ) : (
              <AlertCircle size={32} className="result-icon risk" />
            )}
            <div>
              <h2 className="result-title">Risk Assessment</h2>
              <p className="result-risk">
                Risk Level: <span className={`risk-${getRiskColor(result.risk_level)}`}>
                  {result.risk_level.toUpperCase()}
                </span>
              </p>
            </div>
          </div>

          <div className="result-details">
            <p className="result-survival">
              <strong>Survival Months:</strong> {result.survival_months?.toFixed(1) || months.toFixed(1)}
            </p>
            {result.emergency_fund_status && (
              <p className="result-fund">
                <strong>Emergency Fund:</strong> {result.emergency_fund_status.toUpperCase()}
              </p>
            )}
            <p className="result-advice">{result.advice}</p>
          </div>

          <div className="recommendations">
            <h3>Recommendations</h3>
            <ul>
              {result.risk_level?.toLowerCase() === 'high' ? (
                <>
                  <li>Build up your emergency fund to at least 12 months</li>
                  <li>Create a detailed budget before quitting</li>
                  <li>Consider part-time or freelance work as backup</li>
                </>
              ) : result.risk_level?.toLowerCase() === 'medium' ? (
                <>
                  <li>Ensure you have 6+ months of runway</li>
                  <li>Plan for specific job search timeline</li>
                  <li>Reduce discretionary spending</li>
                </>
              ) : (
                <>
                  <li>You're in a strong financial position</li>
                  <li>Plan your next career move carefully</li>
                  <li>Consider investing unused savings</li>
                </>
              )}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

export default QuitJobPage;
