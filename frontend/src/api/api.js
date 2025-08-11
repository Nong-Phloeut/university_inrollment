// import { useLoadingStore } from '@/stores/loading'
// import { useCommonStore } from '@/stores/common'
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_APP_API_BASE_URL,
  headers: {
    'Access-Control-Allow-Origin': '*',
    'Content-type': 'application/json'
  }
})

// // Get store instance
// const loadingStore = useLoadingStore()
// const tokenExpiredStore = useCommonStore()

// Request Interceptor
api.interceptors.request.use(async config => {
  try {
    // const token = localStorage.getItem('access_token')
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`
    // }
    // loadingStore.setLoading(true)
    return config
  } catch (error) {
    // loadingStore.setLoading(false)
    return Promise.reject(error)
  }
})

// Response Interceptor
api.interceptors.response.use(
  response => {
    // loadingStore.setLoading(false)
    return response
  },

  error => {
    // loadingStore.setLoading(false)
    return Promise.reject(error)
  }
)

export default api
