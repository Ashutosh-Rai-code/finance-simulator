import './ProgressBar.css';

interface ProgressBarProps {
  current: number;
  target: number;
  label?: string;
  showPercentage?: boolean;
}

function ProgressBar({
  current,
  target,
  label,
  showPercentage = true,
}: ProgressBarProps) {
  const percentage = Math.min((current / target) * 100, 100);
  const remaining = target - current;

  const formatCurrency = (value: number) => {
    if (value >= 10000000) return `₹${(value / 10000000).toFixed(1)}Cr`;
    if (value >= 100000) return `₹${(value / 100000).toFixed(1)}L`;
    return `₹${value.toLocaleString()}`;
  };

  return (
    <div className="progress-container">
      {label && <h3 className="progress-label">{label}</h3>}
      
      <div className="progress-info">
        <div>
          <p className="progress-stat">Current: {formatCurrency(current)}</p>
          <p className="progress-stat">Target: {formatCurrency(target)}</p>
        </div>
        {showPercentage && (
          <p className="progress-percentage">{Math.round(percentage)}%</p>
        )}
      </div>

      <div className="progress-bar-container">
        <div
          className="progress-bar-fill"
          style={{ width: `${percentage}%` }}
        >
          <span className="progress-bar-label">
            {percentage > 10 && `${Math.round(percentage)}%`}
          </span>
        </div>
      </div>

      {remaining > 0 && (
        <p className="progress-remaining">
          Remaining: {formatCurrency(remaining)}
        </p>
      )}
    </div>
  );
}

export default ProgressBar;
