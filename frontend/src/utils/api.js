import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || ''

export const apiClient = axios.create({
  baseURL: API_URL,
  timeout: 90000,
})

apiClient.interceptors.request.use((config) => {
  console.log('[API request]', {
    method: config.method,
    url: `${config.baseURL}${config.url}`,
    data: config.data,
  })
  return config
})

apiClient.interceptors.response.use(
  (response) => {
    console.log('[API response]', {
      url: `${response.config.baseURL}${response.config.url}`,
      status: response.status,
      data: response.data,
    })
    return response
  },
  (error) => {
    console.error('[API error]', {
      message: error.message,
      status: error.response?.status,
      data: error.response?.data,
      url: `${error.config?.baseURL || ''}${error.config?.url || ''}`,
    })
    return Promise.reject(error)
  },
)

export async function searchByText({ query, topK = 5 }) {
  const formData = new FormData()
  formData.append('query', query)
  formData.append('top_k', String(topK))
  const response = await apiClient.post('/search', formData)
  return response.data
}

export async function searchByImage({ file, topK = 5 }) {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('top_k', String(topK))

  const response = await apiClient.post('/search', formData)
  return response.data
}

export async function searchHybrid({ file, query, topK = 5 }) {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('query', query)
  formData.append('top_k', String(topK))

  const response = await apiClient.post('/search', formData, {
    timeout: 120000,
  })
  return response.data
}
