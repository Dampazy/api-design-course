import { createContext, useContext, useMemo } from 'react'

const STORAGE_KEY = 'api_course_session_id'

export function getSessionId() {
  let sessionId = localStorage.getItem(STORAGE_KEY)
  if (!sessionId) {
    sessionId = crypto.randomUUID()
    localStorage.setItem(STORAGE_KEY, sessionId)
  }
  return sessionId
}

const SessionContext = createContext(null)

export function SessionProvider({ children }) {
  const sessionId = useMemo(() => getSessionId(), [])
  return (
    <SessionContext.Provider value={sessionId}>
      {children}
    </SessionContext.Provider>
  )
}

export function useSessionId() {
  return useContext(SessionContext)
}
