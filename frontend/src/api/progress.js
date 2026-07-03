import { apiGet } from './client'

export const getProgress = () => apiGet('/progress', { includeSession: true })
export const getFinalTestProgress = () => apiGet('/progress/final-test', { includeSession: true })
export const getStats = () => apiGet('/stats')
