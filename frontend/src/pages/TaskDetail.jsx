import { useEffect, useRef, useState } from 'react'
import { Link, useParams, useSearchParams } from 'react-router-dom'
import { getTask, submitAnswer } from '../api/tasks'
import Markdown from '../components/Markdown.jsx'
import SubmissionResult from '../components/SubmissionResult.jsx'
import MultipleChoiceForm from '../components/answer-forms/MultipleChoiceForm.jsx'
import FillBlankForm from '../components/answer-forms/FillBlankForm.jsx'
import OrderingForm from '../components/answer-forms/OrderingForm.jsx'
import ApiRequestForm from '../components/answer-forms/ApiRequestForm.jsx'

const TEXT_ANSWER_TYPES = ['JSON_FIX', 'FILL_BLANK', 'API_REQUEST']

function defaultAnswerFor(taskType) {
  switch (taskType) {
    case 'MULTIPLE_CHOICE':
      return []
    case 'MATCHING':
      return {}
    case 'ORDERING':
      return null
    default:
      return TEXT_ANSWER_TYPES.includes(taskType) ? '' : null
  }
}

function isAnswerEmpty(taskType, answer) {
  if (taskType === 'SINGLE_CHOICE') return answer === null || answer === undefined
  if (taskType === 'MULTIPLE_CHOICE') return !Array.isArray(answer) || answer.length === 0
  if (taskType === 'MATCHING') return !answer || Object.keys(answer).length === 0
  if (taskType === 'ORDERING') return false
  return !answer || String(answer).trim() === ''
}

export default function TaskDetail() {
  const { taskId } = useParams()
  const [searchParams] = useSearchParams()
  const isFromFinalTest = searchParams.get('final') === '1'

  const [task, setTask] = useState(null)
  const [error, setError] = useState(null)
  const [answer, setAnswer] = useState(null)
  const [result, setResult] = useState(null)
  const [submitting, setSubmitting] = useState(false)
  const startedAtRef = useRef(Date.now())

  useEffect(() => {
    setTask(null)
    setResult(null)
    setError(null)
    startedAtRef.current = Date.now()
    getTask(taskId)
      .then((t) => {
        setTask(t)
        setAnswer(defaultAnswerFor(t.task_type))
      })
      .catch((e) => setError(e.message))
  }, [taskId])

  async function handleSubmit() {
    setSubmitting(true)
    const responseTimeMs = Date.now() - startedAtRef.current
    try {
      const res = await submitAnswer(taskId, answer, responseTimeMs)
      setResult(res)
    } catch (e) {
      setError(e.message)
    } finally {
      setSubmitting(false)
    }
  }

  if (error) return <p className="result-banner result-banner--incorrect">{error}</p>
  if (!task) return <p>Загрузка...</p>

  const backLink = isFromFinalTest ? '/final-test' : '/practice'
  const backLabel = isFromFinalTest ? '← Итоговый тест' : '← Все задания'

  return (
    <div>
      <Link to={backLink} style={{ fontSize: 14 }}>{backLabel}</Link>
      <h1>{task.title}</h1>
      <Markdown>{task.statement_markdown}</Markdown>

      <div style={{ margin: '18px 0' }}>
        {(task.task_type === 'SINGLE_CHOICE' || task.task_type === 'MULTIPLE_CHOICE') && (
          <MultipleChoiceForm
            options={task.options}
            taskType={task.task_type}
            value={answer}
            onChange={setAnswer}
          />
        )}
        {(task.task_type === 'FILL_BLANK' || task.task_type === 'JSON_FIX') && (
          <FillBlankForm taskType={task.task_type} value={answer} onChange={setAnswer} />
        )}
        {task.task_type === 'ORDERING' && (
          <OrderingForm mode="ordering" options={task.options} value={answer} onChange={setAnswer} />
        )}
        {task.task_type === 'MATCHING' && (
          <OrderingForm mode="matching" options={task.options} value={answer} onChange={setAnswer} />
        )}
        {task.task_type === 'API_REQUEST' && (
          <ApiRequestForm value={answer} onChange={setAnswer} />
        )}
      </div>

      {!result && (
        <button
          type="button"
          className="btn"
          onClick={handleSubmit}
          disabled={submitting || isAnswerEmpty(task.task_type, answer)}
        >
          {submitting ? 'Проверка...' : 'Проверить ответ'}
        </button>
      )}

      <SubmissionResult result={result} />

      {result && (
        <div style={{ display: 'flex', gap: 12, marginTop: 12 }}>
          <button
            type="button"
            className="btn btn--secondary"
            onClick={() => {
              startedAtRef.current = Date.now()
              setResult(null)
            }}
          >
            Попробовать снова
          </button>
          <Link to={backLink} className="btn">
            {isFromFinalTest ? 'К итоговому тесту' : 'К списку заданий'}
          </Link>
        </div>
      )}
    </div>
  )
}
