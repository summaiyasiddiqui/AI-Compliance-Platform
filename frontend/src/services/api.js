import axios from 'axios'
import { tokenStorage } from '../utils/tokenStorage'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use(
  (config) => {
    const accessToken = tokenStorage.getAccessToken()

    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`
    }

    return config
  },
  (error) => Promise.reject(error),
)

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (
      error.response?.status === 401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true

      const refreshToken = tokenStorage.getRefreshToken()

      if (!refreshToken) {
        tokenStorage.clearTokens()
        return Promise.reject(error)
      }

      try {
        const response = await axios.post(
          'https://ai-compliance-backend.vercel.app/auth/refresh',
          {
            refresh_token: refreshToken,
          },
        )

        const {
          access_token,
          refresh_token,
        } = response.data

        tokenStorage.setTokens(
          access_token,
          refresh_token,
        )

        originalRequest.headers.Authorization =
          `Bearer ${access_token}`

        return api(originalRequest)
      } catch (refreshError) {
        tokenStorage.clearTokens()

        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  },
)

export default api