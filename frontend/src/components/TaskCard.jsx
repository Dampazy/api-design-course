import { Link } from 'react-router-dom'

const TYPE_LABELS = {
  SINGLE_CHOICE: 'Один вариант',
  MULTIPLE_CHOICE: 'Несколько вариантов',
  FILL_BLANK: 'Заполнить пропуск',
  ORDERING: 'Упорядочить шаги',
  MATCHING: 'Сопоставить пары',
  JSON_FIX: 'Исправить JSON',
  API_REQUEST: 'Написать запрос',
}

export default function TaskCard({ task, solved }) {
  const linkTo = task.is_final_test ? `/practice/${task.id}?final=1` : `/practice/${task.id}`
  return (
    <Link to={linkTo} className="card-link">
      <div className="card">
        <span className="badge">{TYPE_LABELS[task.task_type] || task.task_type}</span>
        {solved && <span className="badge" style={{ marginLeft: 6, color: 'var(--success)' }}>решено</span>}
        <h3 className="card__title">{task.title}</h3>
      </div>
    </Link>
  )
}
