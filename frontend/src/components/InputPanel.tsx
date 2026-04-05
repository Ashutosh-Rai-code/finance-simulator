import { useState } from 'react';
import './InputPanel.css';

interface FinancialData {
  income: number;
  expenses: number;
  savings: number;
  sip: number;
  target_goal: number;
}

interface InputPanelProps {
  initialData: FinancialData;
  onUpdate: (data: FinancialData) => void;
}

function InputPanel({ initialData, onUpdate }: InputPanelProps) {
  const [data, setData] = useState(initialData);

  const handleChange = (field: keyof FinancialData, value: number) => {
    const newData = { ...data, [field]: value };
    setData(newData);
    onUpdate(newData);
  };

  const formatCurrency = (value: number) => {
    if (value >= 100000) return `₹${(value / 100000).toFixed(1)}L`;
    return `₹${value.toLocaleString()}`;
  };

  const inputs = [
    {
      label: 'Monthly Income',
      key: 'income',
      min: 10000,
      max: 500000,
      step: 5000,
    },
    {
      label: 'Monthly Expenses',
      key: 'expenses',
      min: 5000,
      max: 300000,
      step: 5000,
    },
    {
      label: 'Current Savings',
      key: 'savings',
      min: 0,
      max: 5000000,
      step: 50000,
    },
    {
      label: 'Monthly SIP',
      key: 'sip',
      min: 0,
      max: 200000,
      step: 5000,
    },
    {
      label: 'Target Goal',
      key: 'target_goal',
      min: 500000,
      max: 10000000,
      step: 100000,
    },
  ];

  return (
    <div className="input-panel">
      <h3 className="panel-title">📊 Your Financial Profile</h3>
      
      <div className="inputs-grid">
        {inputs.map((input) => (
          <div key={input.key} className="input-group">
            <label className="input-label">{input.label}</label>
            <input
              type="range"
              min={input.min}
              max={input.max}
              step={input.step}
              value={data[input.key as keyof FinancialData]}
              onChange={(e) =>
                handleChange(
                  input.key as keyof FinancialData,
                  parseInt(e.target.value)
                )
              }
              className="input-slider"
            />
            <div className="input-value">
              {formatCurrency(data[input.key as keyof FinancialData])}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default InputPanel;
