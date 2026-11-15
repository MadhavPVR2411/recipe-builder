import { useState } from 'react'
import Login from './Login'

export default function App() {
  const [loggedIn, setLoggedIn] = useState(!!localStorage.getItem('token'))

  function logout() {
    localStorage.removeItem('token')
    setLoggedIn(false)
  }

  if (!loggedIn) return <Login onLogin={() => setLoggedIn(true)} />

  return (
    <div>
      <h1>Recipe Book</h1>
      <button onClick={logout}>Log out</button>
    </div>
  )
}