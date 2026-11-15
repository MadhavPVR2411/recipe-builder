import { useState } from 'react'
import Login from './auth/Login'
import Signup from './auth/Signup'

export default function App() {
  const [loggedIn, setLoggedIn] = useState(!!localStorage.getItem('token'))
  const [showSignup, setShowSignup] = useState(false)

  function logout() {
    localStorage.removeItem('token')
    setLoggedIn(false)
  }

  if (!loggedIn) {
    return showSignup
      ? <Signup onDone={() => setShowSignup(false)} />
      : (
        <>
          <Login onLogin={() => setLoggedIn(true)} />
          <p>No account? <button onClick={() => setShowSignup(true)}>Sign up</button></p>
        </>
      )
  }

  return (
    <div>
      <h1>Recipe Book</h1>
      <button onClick={logout}>Log out</button>
    </div>
  )
}
