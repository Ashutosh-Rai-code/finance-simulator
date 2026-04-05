import { useState, useEffect } from 'react';
import { Menu, X } from 'lucide-react';
import './App.css';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import InsightsPage from './pages/InsightsPage';
import GoalPlannerPage from './pages/GoalPlannerPage';
import SettingsPage from './pages/SettingsPage';

type MenuItem = 'dashboard' | 'insights' | 'goal-planner' | 'settings';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [currentPage, setCurrentPage] = useState<MenuItem>('dashboard');
  const [theme, setTheme] = useState<'light' | 'dark'>('dark');

  const toggleTheme = () => {
    setTheme(theme === 'light' ? 'dark' : 'light');
    document.documentElement.setAttribute('data-theme', theme === 'light' ? 'dark' : 'light');
  };

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  return (
    <div className="app-container">
      <Sidebar
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        currentPage={currentPage}
        onPageChange={setCurrentPage}
      />

      <div className="main-content">
        <header className="app-header">
          <button
            className="sidebar-toggle"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            {sidebarOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
          
          <h1 className="app-title">💰 AI Financial Coach</h1>
          
          <button
            className="theme-toggle"
            onClick={toggleTheme}
            title="Toggle theme"
          >
            {theme === 'light' ? '🌙' : '☀️'}
          </button>
        </header>

        <main className="page-content">
          {currentPage === 'dashboard' && <Dashboard />}
          {currentPage === 'insights' && <InsightsPage />}
          {currentPage === 'goal-planner' && <GoalPlannerPage />}
          {currentPage === 'settings' && <SettingsPage />}
        </main>
      </div>
    </div>
  );
}

export default App;
