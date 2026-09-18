import { createContext, useContext, useEffect, useState } from 'react'
import { getCurrentUser, logoutUser } from '../services/authService'
import { tokenStorage } from '../utils/tokenStorage'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const restoreSession = async () => {
      const accessToken = tokenStorage.getAccessToken()

      if (!accessToken) {
        setLoading(false)
        return
      }

      try {
        const currentUser = await getCurrentUser()
        setUser(currentUser)
      } catch (error) {
        tokenStorage.clearTokens()
        setUser(null)
      } finally {
        setLoading(false)
      }
    }

    restoreSession()
  }, [])

  const login = async (authData) => {
    tokenStorage.setTokens(
      authData.access_token,
      authData.refresh_token,
    )

    const currentUser = await getCurrentUser()

    setUser(currentUser)

    return currentUser
  }

  const logout = async () => {
    try {
      if (tokenStorage.getRefreshToken()) {
        await logoutUser()
      }
    } catch (error) {
      console.error('Logout failed:', error)
    } finally {
      tokenStorage.clearTokens()
      setUser(null)
    }
  }

  const value = {
    user,
    isAuthenticated: user !== null,
    loading,
    login,
    logout,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}