import { useRouter } from 'next/router';
import {
  LayoutDashboard,
  Database,
  Sparkles,
  FlaskConical,
  FileDown,
  Settings,
  HelpCircle,
  Activity,
} from 'lucide-react';

const navItems = [
  { label: 'Dashboard', icon: LayoutDashboard, href: '/' },
  { label: 'Datasets', icon: Database, href: '/datasets' },
  { label: 'Process', icon: Sparkles, href: '/process' },
];

const toolItems = [
  { label: 'Health Score', icon: Activity, href: '/health' },
  { label: 'Exports', icon: FileDown, href: '/exports' },
];

export default function Sidebar() {
  const router = useRouter();

  const NavLink = ({ item }) => {
    const isActive = router.pathname === item.href;
    const Icon = item.icon;
    return (
      <button
        className={`sidebar-link ${isActive ? 'active' : ''}`}
        onClick={() => router.push(item.href)}
      >
        <Icon />
        {item.label}
      </button>
    );
  };

  return (
    <aside className="sidebar">
      {/* Brand */}
      <div className="sidebar-brand">
        <div className="sidebar-brand-icon">DS</div>
        <span className="sidebar-brand-text">DataSanity</span>
      </div>

      {/* Navigation */}
      <nav className="sidebar-nav">
        <div className="sidebar-section-title">Main</div>
        {navItems.map((item) => (
          <NavLink key={item.href} item={item} />
        ))}

        <div className="sidebar-section-title">Tools</div>
        {toolItems.map((item) => (
          <NavLink key={item.href} item={item} />
        ))}
      </nav>

      {/* Footer */}
      <div className="sidebar-footer">
        <button className="sidebar-link" onClick={() => {}}>
          <Settings />
          Settings
        </button>
        <button className="sidebar-link" onClick={() => {}}>
          <HelpCircle />
          Help & Docs
        </button>
      </div>
    </aside>
  );
}
