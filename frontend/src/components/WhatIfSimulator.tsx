import { useState } from 'react';
import { Zap } from 'lucide-react';
import { financialService, FinancialInput } from '../services/api';
import './WhatIfSimulator.css';

interface WhatIfSimulatorProps {
  currentData: FinancialInput;
}

function WhatIfSimulator({ currentData }: WhatIfSimulatorProps) {
  const [newSip, setNewSip] = useState(currentData.sip * 1.5);
  const [rateOfReturn, setRateOfReturn] = useState(12);
  const [durationYears, setDurationYears] = useState(10);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSimulation = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await financialService.whatIfSimulation(
        currentData,
        newSip,
        rateOfReturn,
        durationYears
      );
      setResult(response.data);
    } catch (err: any) {
      console.error('Simulation error:', err);
      setError(err.message || 'Simulation failed.');
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (value: number) => {
    if (value >= 10000000) return `₹${(value / 10000000).toFixed(1)}Cr`;
    if (value >= 100000) return `₹${(value / 100000).toFixed(1)}L`;
    return `₹${value.toLocaleString()}`;
  };

  const formatResultLabel = (value: number) => {
    if (value >= 10000000) return `₹${(value / 10000000).toFixed(1)}Cr`;
    if (value >= 100000) return `₹${(value / 100000).toFixed(1)}L`;
    return `₹${value.toLocaleString()}`;
  };

  return (
    <div className="what-if-simulator">
      <h2 className="section-title">
        <Zap size={24} /> What-If Simulator
      </h2>

      <div className="simulator-content">
        <div className="simulator-input">
          <label className="input-label">New SIP amount</label>
          <input
            type="range"
            min={0}
            max={Math.max(currentData.sip * 3, 50000)}
            step={1000}
            value={newSip}
            onChange={(e) => setNewSip(Number(e.target.value))}
            className="input-slider"
          />
          <div className="slider-range-labels">
            <span className="slider-range-label">{formatCurrency(0)}/mo</span>
            <span className="slider-range-label">{formatCurrency(Math.max(currentData.sip * 3, 50000))}/mo</span>
          </div>
          <p className="slider-value">{formatCurrency(newSip)}/mo</p>

          <label className="input-label">Rate of return (%)</label>
          <input
            type="range"
            min={4}
            max={20}
            step={0.5}
            value={rateOfReturn}
            onChange={(e) => setRateOfReturn(Number(e.target.value))}
            className="input-slider"
          />
          <p className="slider-value">{rateOfReturn.toFixed(1)}%</p>

          <label className="input-label">Duration (years)</label>
          <input
            type="range"
            min={3}
            max={20}
            step={1}
            value={durationYears}
            onChange={(e) => setDurationYears(Number(e.target.value))}
            className="input-slider"
          />
          <p className="slider-value">{durationYears} years</p>

          <div className="sip-display">
            <div>
              <p className="current-sip">Current SIP: {formatCurrency(currentData.sip)}/mo</p>
              <p className="new-sip">New SIP: {formatCurrency(newSip)}/mo</p>
              <p className="increase">
                Increase: {formatCurrency(newSip - currentData.sip)}/mo
              </p>
            </div>
          </div>

          <button
            className="simulate-btn"
            onClick={handleSimulation}
            disabled={loading}
          >
            {loading ? 'Calculating...' : 'Simulate Impact'}
          </button>

          {error && <div className="error-message">{error}</div>}
        </div>

        {result && (
          <div className="simulator-result">
            <div className="result-card">
              <p className="result-label">Final Value ({durationYears} years)</p>
              <div className="result-comparison">
                <div className="result-item">
                  <span className="old-value">
                    {formatResultLabel(result.current_final_value)}
                  </span>
                  <span className="result-desc">Current SIP</span>
                </div>
                <div className="arrow">→</div>
                <div className="result-item">
                  <span className="new-value">
                    {formatResultLabel(result.new_final_value)}
                  </span>
                  <span className="result-desc">New SIP</span>
                </div>
              </div>
            </div>

            <div className="additional-wealth">
              <p className="wealth-label">Additional Wealth Created</p>
              <p className="wealth-value">
                {formatResultLabel(result.additional_wealth)}
              </p>
              <p className="wealth-desc">compared to current SIP</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default WhatIfSimulator;
