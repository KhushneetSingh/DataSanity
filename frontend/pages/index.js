import Head from 'next/head';
import { useState, useEffect, useRef, useCallback } from 'react';
import {
  Database,
  Upload,
  Rows3,
  Columns3,
  Activity,
  FileSpreadsheet,
  ArrowUpRight,
  Trash2,
  Download,
} from 'lucide-react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || '';

function HomePage() {
  const [datasets, setDatasets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef(null);

  /* ─── Fetch datasets ────────────────────────── */
  const fetchDatasets = useCallback(async () => {
    try {
      const res = await fetch(`${API_URL}/api/datasets`);
      if (res.ok) {
        const data = await res.json();
        setDatasets(data.datasets || []);
      }
    } catch (err) {
      console.error('Failed to fetch datasets', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchDatasets();
  }, [fetchDatasets]);

  /* ─── Upload handler ────────────────────────── */
  const handleUpload = async (file) => {
    if (!file) return;
    setUploading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      const res = await fetch(`${API_URL}/api/upload`, {
        method: 'POST',
        body: formData,
      });
      if (res.ok) {
        await fetchDatasets();
      } else {
        const err = await res.json();
        alert(err.detail || 'Upload failed');
      }
    } catch (err) {
      console.error('Upload error', err);
      alert('Upload failed — check console.');
    } finally {
      setUploading(false);
    }
  };

  /* ─── Delete handler ────────────────────────── */
  const handleDelete = async (e, id) => {
    e.stopPropagation();
    if (!confirm('Delete this dataset?')) return;
    try {
      await fetch(`${API_URL}/api/datasets/${id}`, { method: 'DELETE' });
      setDatasets((prev) => prev.filter((d) => d.id !== id));
    } catch (err) {
      console.error('Delete error', err);
    }
  };

  /* ─── Drag & drop ──────────────────────────── */
  const onDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files?.[0];
    if (file && file.name.endsWith('.csv')) handleUpload(file);
  };

  /* ─── Stats ────────────────────────────────── */
  const totalRows = datasets.reduce((s, d) => s + (d.rows || 0), 0);
  const totalCols = datasets.reduce((s, d) => s + (d.columns || 0), 0);
  const avgHealth =
    datasets.length > 0
      ? (datasets.reduce((s, d) => s + (d.health_score || 0), 0) / datasets.length).toFixed(1)
      : '—';

  /* ─── Health color helper ──────────────────── */
  const healthColor = (score) => {
    if (score == null) return 'var(--ds-text-dim)';
    if (score >= 80) return 'var(--ds-green)';
    if (score >= 50) return 'var(--ds-amber)';
    return 'var(--ds-red)';
  };

  const healthBadge = (score) => {
    if (score == null) return 'badge';
    if (score >= 80) return 'badge badge-green';
    if (score >= 50) return 'badge badge-amber';
    return 'badge badge-red';
  };

  const formatBytes = (bytes) => {
    if (!bytes) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  };

  const formatDate = (iso) => {
    if (!iso) return '';
    const d = new Date(iso);
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  };

  return (
    <>
      <Head>
        <title>Dashboard — DataSanity</title>
        <meta name="description" content="AI-powered data operations dashboard. Upload, clean, generate, and enrich datasets." />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      {/* ── Stat cards ────────────────────────── */}
      <div className="stats-grid">
        <div className="stat-card animate-in animate-delay-1">
          <div className="stat-icon indigo"><Database size={22} /></div>
          <div>
            <div className="stat-label">Total Datasets</div>
            <div className="stat-value">{datasets.length}</div>
          </div>
        </div>
        <div className="stat-card animate-in animate-delay-2">
          <div className="stat-icon green"><Rows3 size={22} /></div>
          <div>
            <div className="stat-label">Total Rows</div>
            <div className="stat-value">{totalRows.toLocaleString()}</div>
          </div>
        </div>
        <div className="stat-card animate-in animate-delay-3">
          <div className="stat-icon amber"><Columns3 size={22} /></div>
          <div>
            <div className="stat-label">Total Columns</div>
            <div className="stat-value">{totalCols.toLocaleString()}</div>
          </div>
        </div>
        <div className="stat-card animate-in animate-delay-4">
          <div className="stat-icon red"><Activity size={22} /></div>
          <div>
            <div className="stat-label">Avg. Health</div>
            <div className="stat-value">{avgHealth}</div>
          </div>
        </div>
      </div>

      {/* ── Upload zone ───────────────────────── */}
      <div
        id="upload-zone"
        className={`upload-zone animate-in animate-delay-2 ${dragOver ? 'drag-over' : ''}`}
        onClick={() => fileInputRef.current?.click()}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={onDrop}
        style={{ marginBottom: 32 }}
      >
        <div className="upload-zone-icon">
          <Upload size={26} />
        </div>
        <div className="upload-zone-title">
          {uploading ? 'Uploading…' : 'Drop your CSV here'}
        </div>
        <div className="upload-zone-sub">
          or <span className="accent">click to browse</span> · CSV up to 50 MB
        </div>
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv"
          style={{ display: 'none' }}
          onChange={(e) => handleUpload(e.target.files?.[0])}
          id="file-upload-input"
        />
      </div>

      {/* ── Dataset grid ──────────────────────── */}
      <div className="section-header animate-in animate-delay-3">
        <h2 className="section-title">Your Datasets</h2>
        <span style={{ fontSize: 13, color: 'var(--ds-text-dim)' }}>
          {datasets.length} dataset{datasets.length !== 1 ? 's' : ''}
        </span>
      </div>

      {loading ? (
        <p style={{ color: 'var(--ds-text-dim)', textAlign: 'center', padding: 48 }}>Loading…</p>
      ) : datasets.length === 0 ? (
        <div style={{
          textAlign: 'center',
          padding: '64px 0',
          color: 'var(--ds-text-dim)',
        }}>
          <Database size={40} style={{ margin: '0 auto 12px', opacity: 0.3 }} />
          <p style={{ fontSize: 15, fontWeight: 500 }}>No datasets yet</p>
          <p style={{ fontSize: 13 }}>Upload a CSV above to get started.</p>
        </div>
      ) : (
        <div className="dataset-grid">
          {datasets.map((ds, i) => (
            <div
              key={ds.id}
              className={`dataset-card animate-in animate-delay-${(i % 4) + 1}`}
              id={`dataset-${ds.id}`}
            >
              <div className="dataset-card-header">
                <div className="dataset-card-icon">
                  <FileSpreadsheet size={20} />
                </div>
                <div style={{ display: 'flex', gap: 6 }}>
                  <button
                    className="topbar-icon-btn"
                    title="Delete"
                    onClick={(e) => handleDelete(e, ds.id)}
                    id={`delete-${ds.id}`}
                  >
                    <Trash2 size={14} />
                  </button>
                  <button
                    className="topbar-icon-btn"
                    title="Open"
                    id={`open-${ds.id}`}
                  >
                    <ArrowUpRight size={14} />
                  </button>
                </div>
              </div>

              <div className="dataset-card-name">{ds.filename}</div>
              <div className="dataset-card-meta">
                <span><Rows3 size={12} /> {ds.rows} rows</span>
                <span><Columns3 size={12} /> {ds.columns} cols</span>
                <span>{formatBytes(ds.size_bytes)}</span>
              </div>

              {/* Health bar */}
              <div className="health-bar-label">
                <span className="label">Health</span>
                <span className="value" style={{ color: healthColor(ds.health_score) }}>
                  {ds.health_score != null ? `${ds.health_score}%` : '—'}
                </span>
              </div>
              <div className="health-bar-track">
                <div
                  className="health-bar-fill"
                  style={{
                    width: `${ds.health_score ?? 0}%`,
                    background: healthColor(ds.health_score),
                  }}
                />
              </div>

              <div style={{ marginTop: 12, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span className={healthBadge(ds.health_score)}>
                  {ds.health_score == null ? 'Pending' : ds.health_score >= 80 ? 'Healthy' : ds.health_score >= 50 ? 'Fair' : 'Poor'}
                </span>
                <span style={{ fontSize: 11, color: 'var(--ds-text-dim)' }}>
                  {formatDate(ds.created_at)}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </>
  );
}

HomePage.pageTitle = 'Dashboard';
export default HomePage;