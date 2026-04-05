import {
  LineChart,
  Line,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';
import './RoadmapChart.css';

interface RoadmapData {
  year: number;
  value_in_lakhs: number;
  notes: string;
}

interface RoadmapChartProps {
  data: RoadmapData[];
}

function RoadmapChart({ data }: RoadmapChartProps) {
  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const value = payload[0].value;
      return (
        <div className="custom-tooltip">
          <p className="tooltip-value">₹{value}L</p>
          <p className="tooltip-label">Year {payload[0].payload.year}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="roadmap-chart">
      <div className="chart-container">
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
            <XAxis dataKey="year" stroke="var(--text-muted)" />
            <YAxis stroke="var(--text-muted)" tickFormatter={(value) => `₹${value}L`} />
            <Tooltip content={<CustomTooltip />} />
            <Area
              type="monotone"
              dataKey="value_in_lakhs"
              stroke="var(--primary)"
              fill="rgba(16, 185, 129, 0.15)"
              name="Wealth (₹ Lakhs)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      <div className="roadmap-table">
        <table>
          <thead>
            <tr>
              <th>Year</th>
              <th>Value (₹L)</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {data.map((item, idx) => (
              <tr key={idx} className={idx === data.length - 1 ? 'highlight' : ''}>
                <td className="year-cell">{item.year}</td>
                <td className="value-cell">
                  ₹{item.value_in_lakhs}L
                </td>
                <td className="status-cell">{item.notes}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default RoadmapChart;
