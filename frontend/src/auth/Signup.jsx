import { useState } from 'react'
import { api } from '../api'

export default function Signup({ onDone }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    try {
      await api('/auth/signup', { method: 'POST', body: { username, password } })
      alert('Account created, please log in')
      onDone()
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>Sign up</h2>
      <input placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
      <input type="password" placeholder="Password (min 8)" value={password} onChange={e => setPassword(e.target.value)} />
      <button type="submit">Sign up</button>
      <p>Already have an account? <button type="button" onClick={onDone}>Log in</button></p>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </form>
  )
}
