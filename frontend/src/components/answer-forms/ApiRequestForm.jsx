export default function ApiRequestForm({ value, onChange }) {
  return (
    <div>
      <textarea
        value={value ?? ''}
        onChange={(e) => onChange(e.target.value)}
        placeholder={'METHOD /путь?параметр=значение\n{"опциональное": "тело запроса"}'}
        rows={5}
        spellCheck={false}
        style={{
          width: '100%',
          fontFamily: 'var(--mono)',
          fontSize: 14,
          padding: 12,
          borderRadius: 8,
          border: '1px solid var(--border)',
          resize: 'vertical',
        }}
      />
      <p style={{ fontSize: 13, color: 'var(--text-muted)', marginTop: 6 }}>
        Первая строка — метод и путь запроса (например <code>POST /orders/42/cancel</code>).
        Если нужно тело запроса — добавьте его на следующей строке в формате JSON.
      </p>
    </div>
  )
}
