import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { loginUser } from '../services/authService'
import { useAuth } from '../context/AuthContext'

function Login() {
  const navigate = useNavigate()
  const { login } = useAuth()

  const [formData, setFormData] = useState({
    username: '',
    password: '',
  })

  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChange = (event) => {
    const { name, value } = event.target

    setFormData((previousData) => ({
      ...previousData,
      [name]: value,
    }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()

    setError('')
    setLoading(true)

    try {
      const authData = await loginUser(formData)

      await login(authData)

      navigate('/dashboard')
    } catch (error) {
      const message =
        error.response?.data?.detail ||
        'Login failed. Please check your credentials.'

      setError(message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h1>Welcome Back</h1>

      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="username">Username</label>

          <input
            id="username"
            name="username"
            type="text"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </div>

        <div>
          <label htmlFor="password">Password</label>

          <input
            id="password"
            name="password"
            type="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>

        {error && <p>{error}</p>}

        <button type="submit" disabled={loading}>
          {loading ? 'Signing in...' : 'Sign In'}
        </button>
      </form>

      <p>
        Don't have an account?{' '}
        <button type="button" onClick={() => navigate('/register')}>
          Create Account
        </button>
      </p>
    </div>
  )
}

export default Login