import { useState } from 'react';
import './GoalPlannerPage.css';

function GoalPlannerPage() {
  const [currentSavings, setCurrentSavings] = useState(500000);
  const [goalAmount, setGoalAmount] = useState(1500000);
  const [years, setYears] = useState(5);
  const [rate, setRate] = useState(12);

  const monthlyRate = rate / 100 / 12;
  const months = years * 12;
  const currentFuture = currentSavings * Math.pow(1 + monthlyRate, months);

  const requiredSip = months > 0
    ? Math.max(
      0,
      (goalAmount - currentFuture) * monthlyRate / (Math.pow(1 + monthlyRate, months) - 1)
    )
    : 0;

  const projectedGoal = currentFuture + requiredSip * ((Math.pow(1 + monthlyRate, months) - 1) / monthlyRate);

  const formatCurrency = (value: number) => {
    if (value >= 10000000) return `₹${(value / 10000000).toFixed(1)}Cr`;
    if (value >= 100000) return `₹${(value / 100000).toFixed(1)}L`;
    return `₹${value.toLocaleString()}`;
  };

  return (
    <div className="goal-planner-page">
      <div className="goal-header">
        <h2>🎯 Goal Planner</h2>
        <p>Set a financial goal, choose a timeline, and see the monthly SIP needed.</p>
      </div>

      <div className="goal-grid">
        <div className="goal-card">
          <label>Current Savings</label>
          <input
            type="range"
            min={0}
            max={5000000}
            step={25000}
            value={currentSavings}
            onChange={(e) => setCurrentSavings(Number(e.target.value))}
            className="input-slider"
          />
          <div className="goal-value">{formatCurrency(currentSavings)}</div>
        </div>

        <div className="goal-card">
          <label>Target Goal</label>
          <input
            type="range"
            min={500000}
            max={10000000}
            step={50000}
            value={goalAmount}
            onChange={(e) => setGoalAmount(Number(e.target.value))}
            className="input-slider"
          />
          <div className="goal-value">{formatCurrency(goalAmount)}</div>
        </div>

        <div className="goal-card">
          <label>Timeline (years)</label>
          <input
            type="range"
            min={1}
            max={20}
            step={1}
            value={years}
            onChange={(e) => setYears(Number(e.target.value))}
            className="input-slider"
          />
          <div className="goal-value">{years} years</div>
        </div>

        <div className="goal-card">
          <label>Expected Return</label>
          <input
            type="range"
            min={4}
            max={20}
            step={0.5}
            value={rate}
            onChange={(e) => setRate(Number(e.target.value))}
            className="input-slider"
          />
          <div className="goal-value">{rate.toFixed(1)}%</div>
        </div>
      </div>

      <div className="goal-summary">
        <div className="summary-box">
          <h3>Required Monthly SIP</h3>
          <p>{formatCurrency(requiredSip)}</p>
        </div>
        <div className="summary-box">
          <h3>Projected Value</h3>
          <p>{formatCurrency(projectedGoal)}</p>
        </div>
        <div className="summary-box">
          <h3>Plan Notes</h3>
          <p>
            You need to save {formatCurrency(requiredSip)} per month to reach your goal of {formatCurrency(goalAmount)} in {years} years at {rate.toFixed(1)}%.
          </p>
        </div>
      </div>
    </div>
  );
}

export default GoalPlannerPage;
