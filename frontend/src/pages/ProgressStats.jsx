import { useEffect, useState } from 'react'
import { getFinalTestProgress, getProgress, getStats } from '../api/progress'
import ProgressBar from '../components/ProgressBar.jsx'

export default function ProgressStats() {
  const [progress, setProgress] = useState(null)
  const [finalTest, setFinalTest] = useState(null)
  const [stats, setStats] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    Promise.all([getProgress(), getFinalTestProgress(), getStats()])
      .then(([progressRes, finalTestRes, statsRes]) => {
        setProgress(progressRes)
        setFinalTest(finalTestRes)
        setStats(statsRes)
      })
      .catch((e) => setError(e.message))
  }, [])

  if (error) return <p className="result-banner result-banner--incorrect">{error}</p>
  if (!progress || !finalTest || !stats) return <p>Загрузка...</p>

  return (
    <div>
      <h1>Прогресс</h1>

      <section style={{ marginBottom: 28 }}>
        <h2>Мой прогресс</h2>
        <ProgressBar percent={progress.percent} label={`Практика: ${progress.solved} / ${progress.total_tasks}`} />
        {progress.by_block.map((block) => (
          <div key={block.theory_block_id} style={{ marginTop: 12 }}>
            <ProgressBar percent={block.total ? (100 * block.solved) / block.total : 0} label={`${block.title}: ${block.solved} / ${block.total}`} />
          </div>
        ))}
        <div style={{ marginTop: 12 }}>
          <ProgressBar percent={finalTest.percent} label={`Итоговый тест: ${finalTest.solved} / ${finalTest.total}`} />
        </div>
      </section>

      <section>
        <h2>Аналитика по всем участникам</h2>
        <p style={{ color: 'var(--text-muted)', fontSize: 14 }}>
          Процент верных ответов и среднее время ответа по каждому заданию (по всем сессиям).
        </p>
        <table className="stats-table">
          <thead>
            <tr>
              <th>Задание</th>
              <th>Блок</th>
              <th>Попыток</th>
              <th>% верных</th>
              <th>Ср. время</th>
            </tr>
          </thead>
          <tbody>
            {stats.map((row) => (
              <tr key={row.task_id}>
                <td>{row.title}</td>
                <td>{row.theory_block_title}</td>
                <td>{row.total_attempts}</td>
                <td>{row.total_attempts ? `${row.correct_rate}%` : '—'}</td>
                <td>{row.avg_response_time_ms ? `${(row.avg_response_time_ms / 1000).toFixed(1)} с` : '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  )
}
