import { useState } from 'react'
import Login from './auth/Login'
import Signup from './auth/Signup'
import Pantry from './pantry/Pantry'
import Suggestions from './suggestions/Suggestions'
import Recipes from "./recipes/Recipes.jsx";

export default function App() {
  const [loggedIn, setLoggedIn] = useState(!!localStorage.getItem('token'))
  const [showSignup, setShowSignup] = useState(false)
  const [version, setVersion] = useState(0)

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
      <Pantry onChange={() => setVersion(v => v + 1)} />
      <Suggestions version={version} />
      <Recipes/>
    </div>
  )
}
