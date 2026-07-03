export default function FillBlankForm({ taskType, value, onChange }) {
  if (taskType === 'JSON_FIX') {
    return (
      <textarea
        value={value ?? ''}
        onChange={(e) => onChange(e.target.value)}
        placeholder='{"type": "...", "title": "...", "status": 0}'
        rows={6}
        style={{
          width: '100%',
          fontFamily: 'var(--mono)',
          padding: 10,
          borderRadius: 8,
          border: '1px solid var(--border)',
        }}
      />
    )
  }

  return (
    <input
      type="text"
      value={value ?? ''}
      onChange={(e) => onChange(e.target.value)}
      placeholder="Ваш ответ"
      style={{
        width: '100%',
        padding: '10px 12px',
        borderRadius: 8,
        border: '1px solid var(--border)',
        fontSize: 15,
      }}
    />
  )
}
