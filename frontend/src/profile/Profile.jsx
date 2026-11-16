import { useEffect, useRef, useState } from 'react'
import { api } from '../api'

// Fade-in on scroll, reused from Barterly's profile page
function useReveal(threshold = 0.12) {
  const ref = useRef(null)
  const [visible, setVisible] = useState(false)
  useEffect(() => {
    const el = ref.current
    if (!el) return
    const obs = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) { setVisible(true); obs.disconnect() } },
      { threshold }
    )
    obs.observe(el)
    return () => obs.disconnect()
  }, [threshold])
  return { ref, visible }
}

function Reveal({ children, delay = 0 }) {
  const { ref, visible } = useReveal()
  return (
    <div ref={ref} style={{
      opacity: visible ? 1 : 0,
      transform: visible ? 'translateY(0)' : 'translateY(24px)',
      transition: `opacity 0.55s ease ${delay}ms, transform 0.55s ease ${delay}ms`,
    }}>
      {children}
    </div>
  )
}

const DIETS = [
  { value: 'veg', label: 'Veg' },
  { value: 'egg', label: 'Egg' },
  { value: 'non_veg', label: 'Non-veg' },
]

export default function Profile({ onLogout }) {
  const [me, setMe] = useState(null)
  const [profile, setProfile] = useState(null)
  const [allAllergens, setAllAllergens] = useState([])
  const [message, setMessage] = useState('')

  useEffect(() => {
    Promise.all([api('/auth/me'), api('/profile'), api('/allergens')])
      .then(([meData, profileData, allergens]) => {
        setMe(meData)
        setProfile(profileData)
        setAllAllergens(allergens)
      })
      .catch(err => setMessage(err.message))
  }, [])

  async function changeDiet(diet_type) {
    setProfile(await api('/profile/diet', { method: 'PUT', body: { diet_type } }))
  }

  async function addAllergen(id) {
    if (!id) return
    setProfile(await api(`/profile/allergens/${id}`, { method: 'POST' }))
  }

  async function removeAllergen(id) {
    setProfile(await api(`/profile/allergens/${id}`, { method: 'DELETE' }))
  }

  if (message) return <div className="bg-card border rounded-2xl p-6 text-muted-foreground">{message}</div>
  if (!me || !profile) return <div className="bg-card border rounded-2xl p-6 animate-pulse h-48" />

  const initials = me.username.slice(0, 2).toUpperCase()
  const mine = new Set(profile.allergens.map(a => a.id))
  const addable = allAllergens.filter(a => !mine.has(a.id))

  return (
    <div className="space-y-6">
      <Reveal>
        <div className="bg-card border rounded-2xl shadow-md overflow-hidden">
          {/* Banner + avatar */}
          <div className="h-24 bg-gradient-to-r from-slate-200 to-blue-100 relative">
            <div className="absolute -bottom-10 left-6 w-20 h-20 rounded-full border-4 border-card bg-muted/40 flex items-center justify-center text-2xl font-bold text-primary">
              {initials}
            </div>
          </div>

          <div className="pt-14 px-6 pb-6 space-y-4">
            <div>
              <h2 className="text-xl mb-0">{me.username}</h2>
              <p className="text-sm text-muted-foreground">Recipe Book member</p>
            </div>

            <div className="bg-muted/15 rounded-xl p-4 space-y-5 text-sm">
              {/* Diet */}
              <div className="flex items-start gap-3">
                <span className="text-xl">🥗</span>
                <div className="flex-1">
                  <p className="text-xs text-muted-foreground mb-2">Diet preference</p>
                  <div className="flex gap-2">
                    {DIETS.map(d => (
                      <button
                        key={d.value}
                        onClick={() => changeDiet(d.value)}
                        className={profile.diet_type === d.value
                          ? 'bg-primary text-primary-foreground'
                          : 'bg-card text-primary border'}
                      >
                        {d.label}
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              {/* Allergens */}
              <div className="flex items-start gap-3">
                <span className="text-xl">⚠️</span>
                <div className="flex-1">
                  <p className="text-xs text-muted-foreground mb-2">Allergies</p>
                  <div className="flex flex-wrap gap-2 mb-3">
                    {profile.allergens.length === 0 && <span className="text-muted-foreground">None added</span>}
                    {profile.allergens.map(a => (
                      <span key={a.id} className="inline-flex items-center gap-1 bg-card border rounded-full pl-3 pr-1 py-1 font-semibold">
                        {a.name}
                        <button
                          onClick={() => removeAllergen(a.id)}
                          className="bg-transparent text-muted-foreground px-2 py-0 hover:text-destructive"
                          aria-label={`Remove ${a.name}`}
                        >
                          ×
                        </button>
                      </span>
                    ))}
                  </div>
                  {addable.length > 0 && (
                    <select value="" onChange={e => addAllergen(e.target.value)}>
                      <option value="">Add an allergy…</option>
                      {addable.map(a => <option key={a.id} value={a.id}>{a.name}</option>)}
                    </select>
                  )}
                </div>
              </div>
            </div>

            <div className="flex justify-end">
              <button onClick={onLogout} className="bg-destructive text-destructive-foreground">
                Log out
              </button>
            </div>
          </div>
        </div>
      </Reveal>
    </div>
  )
}
