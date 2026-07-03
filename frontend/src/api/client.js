import { getSessionId } from '../context/SessionContext'

const BASE_URL = '/api'

async function request(path, { method = 'GET', body, includeSession = false } = {}) {
  const headers = { 'Content-Type': 'application/json' }
  if (includeSession) {
    headers['X-Session-Id'] = getSessionId()
  }

  const response = await fetch(`${BASE_URL}${path}`, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  })

  if (!response.ok) {
    const detail = await response.json().catch(() => ({}))
    throw new Error(detail.detail || `Request failed with status ${response.status}`)
  }

  if (response.status === 204) return null
  return response.json()
}

export const apiGet = (path, opts) => request(path, { method: 'GET', ...opts })
export const apiPost = (path, body, opts) => request(path, { method: 'POST', body, ...opts })
