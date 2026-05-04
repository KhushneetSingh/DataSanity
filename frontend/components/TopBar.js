import { Search, Bell, Moon } from 'lucide-react';
import { useState } from 'react';

export default function TopBar({ title = 'Dashboard' }) {
  const [searchValue, setSearchValue] = useState('');

  return (
    <header className="topbar">
      <h1 className="topbar-title">{title}</h1>

      <div className="topbar-actions">
        {/* Search */}
        <div className="topbar-search">
          <Search size={15} />
          <input
            type="text"
            placeholder="Search datasets…"
            value={searchValue}
            onChange={(e) => setSearchValue(e.target.value)}
            id="global-search"
          />
        </div>

        {/* Icon buttons */}
        <button className="topbar-icon-btn" aria-label="Toggle dark mode" id="theme-toggle">
          <Moon size={16} />
        </button>
        <button className="topbar-icon-btn" aria-label="Notifications" id="notifications-btn">
          <Bell size={16} />
        </button>

        {/* Avatar */}
        <div className="topbar-avatar" id="user-avatar">U</div>
      </div>
    </header>
  );
}
