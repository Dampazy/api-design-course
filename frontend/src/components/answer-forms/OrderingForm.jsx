export default function OrderingForm({ mode, options, value, onChange }) {
  if (mode === 'matching') {
    const left = options?.left ?? []
    const right = options?.right ?? []
    const mapping = value && typeof value === 'object' ? value : {}

    function setMatch(leftIndex, rightIndex) {
      onChange({ ...mapping, [leftIndex]: rightIndex })
    }

    return (
      <div>
        {left.map((leftLabel, leftIndex) => (
          <div key={leftIndex} className="matching-row">
            <span style={{ flex: 1 }}>{leftLabel}</span>
            <select
              value={mapping[leftIndex] ?? ''}
              onChange={(e) => setMatch(leftIndex, Number(e.target.value))}
            >
              <option value="" disabled>
                выберите...
              </option>
              {right.map((rightLabel, rightIndex) => (
                <option key={rightIndex} value={rightIndex}>
                  {rightLabel}
                </option>
              ))}
            </select>
          </div>
        ))}
      </div>
    )
  }

  const items = options?.items ?? []
  const order = Array.isArray(value) && value.length === items.length ? value : items.map((_, i) => i)

  function move(position, direction) {
    const next = [...order]
    const target = position + direction
    if (target < 0 || target >= next.length) return
    ;[next[position], next[target]] = [next[target], next[position]]
    onChange(next)
  }

  return (
    <ol className="ordering-list">
      {order.map((itemIndex, position) => (
        <li key={itemIndex} className="ordering-item">
          <span>{position + 1}.</span>
          <span>{items[itemIndex]}</span>
          <div className="ordering-item__buttons">
            <button type="button" onClick={() => move(position, -1)} disabled={position === 0} aria-label="Вверх">
              ↑
            </button>
            <button
              type="button"
              onClick={() => move(position, 1)}
              disabled={position === order.length - 1}
              aria-label="Вниз"
            >
              ↓
            </button>
          </div>
        </li>
      ))}
    </ol>
  )
}
