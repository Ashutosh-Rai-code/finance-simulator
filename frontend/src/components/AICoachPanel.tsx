import { useState } from 'react';
import { Brain, Loader } from 'lucide-react';
import { aiService, FinancialInput } from '../services/api';
import './AICoachPanel.css';

interface Advice {
  immediate_actions?: string[];
  ninety_day_plan?: string[];
  one_year_vision?: string;
  error?: string;
}

interface AIPanelProps {
  data: FinancialInput;
}

function AICoachPanel({ data }: AIPanelProps) {
  const [advice, setAdvice] = useState<Advice | null>(null);
  const [loading, setLoading] = useState(false);

  const getAdvice = async () => {
    setLoading(true);
    try {
      const response = await aiService.getAdvice(data);
      setAdvice(response.data);
    } catch (error) {
      console.error('AI error:', error);
      setAdvice({ error: 'Failed to get AI advice' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="ai-coach-panel">
      <div className="panel-header">
        <h2 className="section-title">
          <Brain size={24} /> AI Financial Coach
        </h2>
        <button
          className="advice-btn"
          onClick={getAdvice}
          disabled={loading}
        >
          {loading ? (
            <>
              <Loader size={16} className="spinner-icon" />
              Getting advice...
            </>
          ) : (
            '💡 Get Personalized Advice'
          )}
        </button>
      </div>

      {advice && (
        <div className="advice-content">
          {advice.error ? (
            <div className="error-message">{advice.error}</div>
          ) : (
            <>
              {advice.immediate_actions?.length ? (
                <div className="advice-section immediate">
                  <h3 className="advice-heading">⚡ Next 30 Days</h3>
                  <ul className="advice-list">
                    {advice.immediate_actions.map((action, idx) => (
                      <li key={idx} className="advice-item">
                        <span className="item-number">{idx + 1}</span>
                        <span>{action}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              ) : null}

              {advice.ninety_day_plan?.length ? (
                <div className="advice-section plan">
                  <h3 className="advice-heading">📅 90-Day Plan</h3>
                  <ul className="advice-list">
                    {advice.ninety_day_plan.map((action, idx) => (
                      <li key={idx} className="advice-item">
                        <span className="item-number">{idx + 1}</span>
                        <span>{action}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              ) : null}

              {advice.one_year_vision ? (
                <div className="advice-section vision">
                  <h3 className="advice-heading">🎯 1-Year Vision</h3>
                  <p className="vision-text">{advice.one_year_vision}</p>
                </div>
              ) : null}

              {!advice.immediate_actions?.length && !advice.ninety_day_plan?.length && !advice.one_year_vision && (
                <div className="advice-empty">No advice available yet. Try again in a moment.</div>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default AICoachPanel;
