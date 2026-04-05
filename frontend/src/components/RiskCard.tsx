import { AlertCircle, CheckCircle, AlertTriangle } from 'lucide-react';
import './RiskCard.css';

interface Risk {
  risk: string;
  recommendation: string;
  severity: 'low' | 'medium' | 'high';
}

interface RiskCardProps {
  risks: Risk[];
}

function RiskCard({ risks }: RiskCardProps) {
  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'high':
        return <AlertCircle className="severity-high" size={20} />;
      case 'medium':
        return <AlertTriangle className="severity-medium" size={20} />;
      case 'low':
      default:
        return <CheckCircle className="severity-low" size={20} />;
    }
  };

  return (
    <div className="risk-card">
      <h3 className="risk-title">Risk Analysis</h3>
      
      {risks.length === 0 ? (
        <div className="no-risks">
          <CheckCircle size={48} />
          <p>✨ All green! Your financial health looks good.</p>
        </div>
      ) : (
        <div className="risks-list">
          {risks.map((risk, idx) => (
            <div key={idx} className={`risk-item severity-${risk.severity}`}>
              <div className="risk-header">
                {getSeverityIcon(risk.severity)}
                <span className="risk-text">{risk.risk}</span>
              </div>
              <p className="recommendation">💡 {risk.recommendation}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default RiskCard;
