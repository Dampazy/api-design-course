export default function ProgressBar({ percent, label }) {
  const clamped = Math.max(0, Math.min(100, percent))
  return (
    <div>
      {label && (
        <div style={{ fontSize: 14, color: 'var(--text-muted)', marginBottom: 6 }}>
          {label}
        </div>
      )}
      <div className="progress-bar" role="progressbar" aria-valuenow={clamped} aria-valuemin={0} aria-valuemax={100}>
        <div className="progress-bar__fill" style={{ width: `${clamped}%` }} />
      </div>
    </div>
  )
}
