import { useState } from 'react'
import Login from './auth/Login'
import Signup from './auth/Signup'
import Pantry from './pantry/Pantry'
import Suggestions from './suggestions/Suggestions'
import Recipes from './recipes/Recipes'
import Profile from './profile/Profile'

const TABS = [
  { id: 'pantry', label: 'Pantry' },
  { id: 'cook', label: 'What can I cook?' },
  { id: 'recipes', label: 'Recipes' },
  { id: 'profile', label: 'Profile' },
]

export default function App() {
  const [loggedIn, setLoggedIn] = useState(!!localStorage.getItem('token'))
  const [showSignup, setShowSignup] = useState(false)
  const [tab, setTab] = useState('pantry')

  function logout() {
    localStorage.removeItem('token')
    setLoggedIn(false)
    setTab('pantry')
  }

  if (!loggedIn) {
    return (
      <div className="max-w-md mx-auto mt-24 bg-card border rounded-2xl shadow-md p-6 space-y-4">
        <h1>Recipe Book</h1>
        {showSignup
          ? <Signup onDone={() => setShowSignup(false)} />
          : (
            <>
              <Login onLogin={() => setLoggedIn(true)} />
              <p className="text-sm">
                No account?{' '}
                <button onClick={() => setShowSignup(true)} className="bg-transparent text-accent underline p-0">Sign up</button>
              </p>
            </>
          )}
      </div>
    )
  }

  return (
    <div className="max-w-3xl mx-auto px-6 py-8 space-y-6">
      <header className="flex flex-wrap items-center justify-between gap-4">
        <h1>Recipe Book</h1>
        <nav className="flex flex-wrap gap-2">
          {TABS.map(t => (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              className={tab === t.id ? 'bg-primary text-primary-foreground' : 'bg-card text-primary border'}
            >
              {t.label}
            </button>
          ))}
        </nav>
      </header>

      <main className="bg-card border rounded-2xl shadow-sm p-6">
        {tab === 'pantry' && <Pantry onChange={() => {}} />}
        {tab === 'cook' && <Suggestions />}
        {tab === 'recipes' && <Recipes />}
        {tab === 'profile' && <Profile onLogout={logout} />}
      </main>
    </div>
  )
}
