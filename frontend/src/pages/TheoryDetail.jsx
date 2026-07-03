import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { getTheoryBlock, listTheoryBlocks } from '../api/theory'
import Markdown from '../components/Markdown.jsx'
import TheoryNav from '../components/TheoryNav.jsx'

// The page already renders block.title as its own <h1>; the markdown body
// also starts with a top-level "# Title" heading (authored that way so the
// same content reads well standalone, e.g. in the student-guide export).
// Strip that leading heading here to avoid showing the title twice.
function stripLeadingHeading(markdown) {
  return markdown.replace(/^#\s+.+\n+/, '')
}

export default function TheoryDetail() {
  const { slug } = useParams()
  const [block, setBlock] = useState(null)
  const [allBlocks, setAllBlocks] = useState([])
  const [error, setError] = useState(null)

  useEffect(() => {
    setBlock(null)
    setError(null)
    getTheoryBlock(slug).then(setBlock).catch((e) => setError(e.message))
  }, [slug])

  useEffect(() => {
    listTheoryBlocks().then(setAllBlocks).catch(() => {})
  }, [])

  if (error) return <p className="result-banner result-banner--incorrect">{error}</p>
  if (!block) return <p>Загрузка...</p>

  return (
    <div>
      <Link to="/theory" style={{ fontSize: 14 }}>← Все темы</Link>
      <h1>{block.title}</h1>
      <Markdown>{stripLeadingHeading(block.content_markdown)}</Markdown>
      {allBlocks.length > 0 && <TheoryNav blocks={allBlocks} currentSlug={slug} />}
      <div style={{ marginTop: 24 }}>
        <Link to="/practice" className="btn">Перейти к практике →</Link>
      </div>
    </div>
  )
}
