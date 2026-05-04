import Sidebar from './Sidebar';
import TopBar from './TopBar';

export default function Layout({ children, title }) {
  return (
    <div className="app-shell">
      <Sidebar />
      <div className="main-content">
        <TopBar title={title} />
        <main className="page">
          {children}
        </main>
      </div>
    </div>
  );
}
