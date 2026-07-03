import { useEffect, useState } from 'react'
import { listTheoryBlocks } from '../api/theory'
import { listTasks } from '../api/tasks'
import { getProgress } from '../api/progress'
import TaskCard from '../components/TaskCard.jsx'
import ProgressBar from '../components/ProgressBar.jsx'

export default function PracticeList() {
  const [blocks, setBlocks] = useState(null)
  const [tasks, setTasks] = useState(null)
  const [progress, setProgress] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    Promise.all([
      listTheoryBlocks(),
      listTasks({ isFinalTest: false }),
      getProgress(),
    ])
      .then(([blocksRes, tasksRes, progressRes]) => {
        setBlocks(blocksRes)
        setTasks(tasksRes)
        setProgress(progressRes)
      })
      .catch((e) => setError(e.message))
  }, [])

  if (error) return <p className="result-banner result-banner--incorrect">{error}</p>
  if (!blocks || !tasks) return <p>Загрузка...</p>

  const solvedTaskIds = new Set(progress?.solved_task_ids ?? [])

  return (
    <div>
      <h1>Практика</h1>
      {progress && (
        <div style={{ marginBottom: 20 }}>
          <ProgressBar
            percent={progress.percent}
            label={`Решено ${progress.solved} из ${progress.total_tasks} заданий`}
          />
        </div>
      )}
      {blocks.map((block) => {
        const blockTasks = tasks.filter((t) => t.theory_block_id === block.id)
        if (blockTasks.length === 0) return null
        return (
          <section key={block.id} style={{ marginBottom: 28 }}>
            <h2>{block.title}</h2>
            {blockTasks.map((task) => (
              <TaskCard key={task.id} task={task} solved={solvedTaskIds.has(task.id)} />
            ))}
          </section>
        )
      })}
    </div>
  )
}
