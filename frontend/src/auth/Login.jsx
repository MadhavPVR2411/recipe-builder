import { useState } from 'react'
import { api } from '../api'

export default function Login({ onLogin }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    try {
      const data = await api('/auth/login', { method: 'POST', body: { username, password } })
      localStorage.setItem('token', data.access_token)
      onLogin()
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>Log in</h2>
      <input placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
      <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
      <button type="submit">Log in</button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </form>
  )
}