import Markdown from './Markdown.jsx'

export default function SubmissionResult({ result }) {
  if (!result) return null

  return (
    <div className={`result-banner ${result.is_correct ? 'result-banner--correct' : 'result-banner--incorrect'}`}>
      <strong>{result.is_correct ? 'Верно!' : 'Неверно'}</strong>
      {' '}(баллы: {Math.round(result.score * 100)}%)
      {result.explanation_markdown && <Markdown>{result.explanation_markdown}</Markdown>}
    </div>
  )
}
