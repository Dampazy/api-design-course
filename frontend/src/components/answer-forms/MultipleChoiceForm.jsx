export default function MultipleChoiceForm({ options, taskType, value, onChange }) {
  const choices = options?.choices ?? []
  const isMultiple = taskType === 'MULTIPLE_CHOICE'

  function toggle(index) {
    if (isMultiple) {
      const current = Array.isArray(value) ? value : []
      const next = current.includes(index)
        ? current.filter((i) => i !== index)
        : [...current, index]
      onChange(next)
    } else {
      onChange(index)
    }
  }

  const selected = isMultiple ? (Array.isArray(value) ? value : []) : value

  return (
    <div>
      {choices.map((choice, index) => {
        const isSelected = isMultiple ? selected.includes(index) : selected === index
        return (
          <div
            key={index}
            className={`choice-option ${isSelected ? 'choice-option--selected' : ''}`}
            onClick={() => toggle(index)}
          >
            <input
              type={isMultiple ? 'checkbox' : 'radio'}
              checked={isSelected}
              onChange={() => toggle(index)}
              onClick={(e) => e.stopPropagation()}
            />
            <span>{choice}</span>
          </div>
        )
      })}
    </div>
  )
}
