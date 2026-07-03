import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { listTheoryBlocks } from '../api/theory'

export default function TheoryList() {
  const [blocks, setBlocks] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    listTheoryBlocks().then(setBlocks).catch((e) => setError(e.message))
  }, [])

  if (error) return <p className="result-banner result-banner--incorrect">{error}</p>
  if (!blocks) return <p>Загрузка...</p>

  return (
    <div>
      <h1>Теория</h1>
      {blocks.map((block) => (
        <Link key={block.id} to={`/theory/${block.slug}`} className="card-link">
          <div className="card">
            <span className="badge">Блок {block.order_index}</span>
            <h3 className="card__title">{block.title}</h3>
            <p className="card__summary">{block.summary}</p>
          </div>
        </Link>
      ))}
    </div>
  )
}
