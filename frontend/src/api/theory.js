import { apiGet } from './client'

export const listTheoryBlocks = () => apiGet('/theory')
export const getTheoryBlock = (slug) => apiGet(`/theory/${slug}`)
