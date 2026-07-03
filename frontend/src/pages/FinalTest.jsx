import { useEffect, useState } from 'react'
import { listTasks } from '../api/tasks'
import { getFinalTestProgress } from '../api/progress'
import TaskCard from '../components/TaskCard.jsx'
import ProgressBar from '../components/ProgressBar.jsx'

export default function FinalTest() {
  const [tasks, setTasks] = useState(null)
  const [progress, setProgress] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    Promise.all([listTasks({ isFinalTest: true }), getFinalTestProgress()])
      .then(([tasksRes, progressRes]) => {
        setTasks(tasksRes)
        setProgress(progressRes)
      })
      .catch((e) => setError(e.message))
  }, [])

  if (error) return <p className="result-banner result-banner--incorrect">{error}</p>
  if (!tasks) return <p>Загрузка...</p>

  return (
    <div>
      <h1>Итоговый тест</h1>
      <p style={{ color: 'var(--text-muted)' }}>
        {tasks.length} вопросов по всем темам курса. Тест считается пройденным
        при верном ответе минимум на 70% вопросов.
      </p>
      {progress && (
        <div style={{ margin: '16px 0 24px' }}>
          <ProgressBar
            percent={progress.percent}
            label={`Верно решено ${progress.solved} из ${progress.total}`}
          />
          <p style={{ marginTop: 8, fontWeight: 600, color: progress.passed ? 'var(--success)' : 'var(--text-muted)' }}>
            {progress.passed ? 'Тест пройден ✓' : 'Тест ещё не пройден'}
          </p>
        </div>
      )}
      {tasks.map((task) => (
        <TaskCard key={task.id} task={task} solved={progress?.solved_task_ids.includes(task.id) ?? false} />
      ))}
    </div>
  )
}
