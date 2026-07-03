import { Link } from 'react-router-dom'

export default function TheoryNav({ blocks, currentSlug }) {
  const index = blocks.findIndex((b) => b.slug === currentSlug)
  const prev = index > 0 ? blocks[index - 1] : null
  const next = index >= 0 && index < blocks.length - 1 ? blocks[index + 1] : null

  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 24 }}>
      {prev ? (
        <Link to={`/theory/${prev.slug}`} className="btn btn--secondary">
          ← {prev.title}
        </Link>
      ) : (
        <span />
      )}
      {next ? (
        <Link to={`/theory/${next.slug}`} className="btn btn--secondary">
          {next.title} →
        </Link>
      ) : (
        <span />
      )}
    </div>
  )
}
