import { ReactNode } from 'react';
import './MetricsCard.css';

interface MetricsCardProps {
  title: string;
  value: string | number;
  icon?: string | ReactNode;
  subtitle?: string;
  trend?: 'up' | 'down' | 'neutral';
  trendValue?: string;
}

function MetricsCard({
  title,
  value,
  icon,
  subtitle,
  trend,
  trendValue,
}: MetricsCardProps) {
  return (
    <div className={`metrics-card ${trend ? `trend-${trend}` : ''}`}>
      <div className="card-header">
        <h3 className="card-title">{title}</h3>
        {icon && <div className="card-icon">{icon}</div>}
      </div>
      
      <div className="card-value">{value}</div>
      
      {subtitle && <p className="card-subtitle">{subtitle}</p>}
      
      {trendValue && trend && (
        <div className={`trend-indicator trend-${trend}`}>
          <span className="trend-value">{trendValue}</span>
        </div>
      )}
    </div>
  );
}

export default MetricsCard;
