import { apiGet, apiPost } from './client'

export function listTasks({ theoryBlockId, isFinalTest } = {}) {
  const params = new URLSearchParams()
  if (theoryBlockId !== undefined) params.set('theory_block_id', theoryBlockId)
  if (isFinalTest !== undefined) params.set('is_final_test', isFinalTest)
  const query = params.toString()
  return apiGet(`/tasks${query ? `?${query}` : ''}`)
}

export const getTask = (id) => apiGet(`/tasks/${id}`)

export const submitAnswer = (id, answer, responseTimeMs) =>
  apiPost(`/tasks/${id}/submit`, { answer, response_time_ms: responseTimeMs }, { includeSession: true })
