import { BarChart3, TrendingUp, Target, Settings } from 'lucide-react';
import './Sidebar.css';

type MenuItem = 'dashboard' | 'insights' | 'goal-planner' | 'settings';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
  currentPage: MenuItem;
  onPageChange: (page: MenuItem) => void;
}

function Sidebar({ isOpen, onClose, currentPage, onPageChange }: SidebarProps) {
  const menuItems: Array<{ id: MenuItem; label: string; icon: any }> = [
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3 },
    { id: 'insights', label: 'Insights', icon: TrendingUp },
    { id: 'goal-planner', label: 'Goal Planner', icon: Target },
  ];

  const handleMenuClick = (pageId: 'dashboard' | 'insights' | 'goal-planner' | 'settings') => {
    onPageChange(pageId);
    onClose();
  };

  return (
    <>
      {isOpen && (
        <div className="sidebar-overlay" onClick={onClose} />
      )}
      
      <aside className={`sidebar ${isOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <h2>Financial Coach</h2>
        </div>

        <nav className="sidebar-nav">
          {menuItems.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.id}
                className={`nav-item ${currentPage === item.id ? 'active' : ''}`}
                onClick={() => handleMenuClick(item.id)}
              >
                <Icon size={20} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        <div className="sidebar-footer">
          <button className="settings-btn" onClick={() => handleMenuClick('settings')}>
            <Settings size={20} />
            <span>Settings</span>
          </button>
        </div>
      </aside>
    </>
  );
}

export default Sidebar;
