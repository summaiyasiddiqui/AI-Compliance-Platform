import api from './api'

export const loginUser = async (credentials) => {
  const formData = new URLSearchParams()

  formData.append('username', credentials.username)
  formData.append('password', credentials.password)

  const response = await api.post('/auth/login', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  })

  return response.data
}
export const registerUser = async (userData) => {
  const response = await api.post('/auth/register', userData)
  return response.data
}

export const getCurrentUser = async () => {
  const response = await api.get('/auth/me')
  return response.data
}

export const refreshAccessToken = async (refreshToken) => {
  const response = await api.post('/auth/refresh', {
    refresh_token: refreshToken,
  })

  return response.data
}

export const logoutUser = async () => {
  const response = await api.post('/auth/logout')
  return response.data
}