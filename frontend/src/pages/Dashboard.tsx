import { useState, useEffect } from 'react';
import { Zap, TrendingUp, Target } from 'lucide-react';
import InputPanel from '../components/InputPanel';
import MetricsCard from '../components/MetricsCard';
import ProgressBar from '../components/ProgressBar';
import RiskCard from '../components/RiskCard';
import RoadmapChart from '../components/RoadmapChart';
import AICoachPanel from '../components/AICoachPanel';
import WhatIfSimulator from '../components/WhatIfSimulator';
import { financialService, aiService } from '../services/api';
import './Dashboard.css';

interface FinancialData {
  income: number;
  expenses: number;
  savings: number;
  sip: number;
  target_goal: number;
}

interface Metrics {
  savings_rate: number;
  emergency_months: number;
  sip_ratio: number;
  monthly_surplus: number;
  goal_progress: number;
}

function Dashboard() {
  const [data, setData] = useState<FinancialData>({
    income: 100000,
    expenses: 50000,
    savings: 500000,
    sip: 20000,
    target_goal: 1000000,
  });

  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [risks, setRisks] = useState<any[]>([]);
  const [roadmap, setRoadmap] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchData = async (financialData: FinancialData) => {
    setLoading(true);
    try {
      const [metricsRes, risksRes, roadmapRes] = await Promise.all([
        financialService.calculateMetrics(financialData),
        financialService.analyzeRisks(financialData),
        financialService.getRoadmap(financialData),
      ]);

      setMetrics(metricsRes.data);
      setRisks(risksRes.data.risks || []);
      setRoadmap(roadmapRes.data.roadmap || []);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData(data);
  }, [data]);

  const handleDataUpdate = (newData: FinancialData) => {
    setData(newData);
  };

  const formatCurrency = (value: number) => {
    if (value >= 10000000) return `₹${(value / 10000000).toFixed(1)}Cr`;
    if (value >= 100000) return `₹${(value / 100000).toFixed(1)}L`;
    return `₹${value.toLocaleString()}`;
  };

  return (
    <div className="dashboard">
      <InputPanel initialData={data} onUpdate={handleDataUpdate} />

      {loading ? (
        <div className="loading">
          <div className="spinner"></div>
          <p>Analyzing your finances...</p>
        </div>
      ) : (
        <>
          {/* Metrics Overview */}
          <section className="metrics-section">
            <h2 className="section-title">📊 Financial Metrics</h2>
            <div className="metrics-grid">
              <MetricsCard
                title="Monthly Income"
                value={formatCurrency(data.income)}
                icon="💼"
                trend="up"
              />
              <MetricsCard
                title="Monthly Expenses"
                value={formatCurrency(data.expenses)}
                icon="💸"
                trend="down"
              />
              <MetricsCard
                title="Savings Rate"
                value={metrics ? `${metrics.savings_rate.toFixed(1)}%` : '-'}
                icon="📈"
                subtitle={metrics ? `Target: 30%` : ''}
                trend={metrics && metrics.savings_rate >= 30 ? 'up' : 'down'}
              />
              <MetricsCard
                title="Emergency Fund"
                value={metrics ? `${metrics.emergency_months.toFixed(1)} mo` : '-'}
                icon="🛡️"
                subtitle={metrics ? `Target: 6 months` : ''}
                trend={metrics && metrics.emergency_months >= 6 ? 'up' : 'down'}
              />
              <MetricsCard
                title="SIP Ratio"
                value={metrics ? `${metrics.sip_ratio.toFixed(1)}%` : '-'}
                icon="💹"
                subtitle={metrics ? `Target: 20%` : ''}
                trend={metrics && metrics.sip_ratio >= 20 ? 'up' : 'down'}
              />
              <MetricsCard
                title="Monthly Surplus"
                value={metrics ? formatCurrency(metrics.monthly_surplus) : '-'}
                icon="💰"
                trend="up"
              />
            </div>
          </section>

          {/* Goal Progress */}
          <section className="goal-section">
            <ProgressBar
              current={data.savings}
              target={data.target_goal}
              label="🎯 Goal Progress"
              showPercentage={true}
            />
          </section>

          {/* Risk Analysis */}
          <section className="risk-section">
            <RiskCard risks={risks} />
          </section>

          {/* Roadmap */}
          <section className="roadmap-section">
            <h2 className="section-title">📈 Wealth Roadmap</h2>
            {roadmap.length > 0 && <RoadmapChart data={roadmap} />}
          </section>

          {/* What If Simulator */}
          <section className="simulator-section">
            <WhatIfSimulator currentData={data} />
          </section>

          {/* AI Coach */}
          <section className="ai-section">
            <AICoachPanel data={data} />
          </section>
        </>
      )}
    </div>
  );
}

export default Dashboard;
