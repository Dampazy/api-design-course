import { Link } from 'react-router-dom'

export default function Home() {
  return (
    <div>
      <h1>Проектирование API</h1>
      <p style={{ color: 'var(--text-muted)', maxWidth: 640 }}>
        Интерактивный учебный курс по принципам проектирования REST API: 6
        теоретических блоков, 18 практических заданий с автопроверкой и
        итоговый тест. Пройдите теорию, закрепите знания на практике и
        отслеживайте свой прогресс.
      </p>
      <div style={{ display: 'flex', gap: 12, marginTop: 20 }}>
        <Link to="/theory" className="btn">Начать с теории</Link>
        <Link to="/practice" className="btn btn--secondary">Перейти к практике</Link>
      </div>
    </div>
  )
}
