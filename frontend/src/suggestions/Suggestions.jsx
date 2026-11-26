import { useEffect, useState } from 'react'
import { api } from '../api'
import RecipeDetail from '../recipes/RecipeDetail'

const TIMES = [
  { label: '15 min', value: 15 },
  { label: '30 min', value: 30 },
  { label: '1 hour', value: 60 },
  { label: 'No rush', value: null },
]

function Chip({ active, onClick, children }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={active ? 'bg-primary text-primary-foreground' : 'bg-card text-primary border'}
    >
      {children}
    </button>
  )
}

function RecipeCard({ recipe, note, onOpen }) {
  return (
    <li>
      <button
        type="button"
        onClick={() => onOpen(recipe.id)}
        className="w-full h-full text-left bg-card text-foreground border rounded-xl p-4 font-normal hover:border-primary hover:shadow-sm"
      >
        <p className="font-semibold">{recipe.name}</p>
        <p className="text-sm text-muted-foreground">
          {recipe.cuisine} | {recipe.total_time} min | {recipe.complexity}
        </p>
        {note && <p className="text-sm mt-2">{note}</p>}
      </button>
    </li>
  )
}

export default function Suggestions() {
  const [cuisines, setCuisines] = useState([])
  const [cuisine, setCuisine] = useState(null)
  const [maxTime, setMaxTime] = useState(null)
  const [data, setData] = useState({ can_make: [], missing_one: [] })
  const [openId, setOpenId] = useState(null)

  useEffect(() => {
    api('/recipes').then(recipes => {
      setCuisines([...new Set(recipes.map(r => r.cuisine))].sort())
    })
  }, [])

  useEffect(() => {
    const params = new URLSearchParams()
    if (cuisine) params.set('cuisine', cuisine)
    if (maxTime) params.set('max_time', maxTime)
    const query = params.toString()
    api(query ? `/suggestions?${query}` : '/suggestions').then(setData)
  }, [cuisine, maxTime])

  if (openId) {
    return <RecipeDetail recipeId={openId} onBack={() => setOpenId(null)} backLabel="Back to suggestions" />
  }

  const nothing = data.can_make.length === 0 && data.missing_one.length === 0

  return (
    <section className="space-y-6">
      <div className="space-y-3">
        <h2 className="mb-0">What are we in the mood for?</h2>
        <div className="flex flex-wrap gap-2">
          <Chip active={cuisine === null} onClick={() => setCuisine(null)}>Anything</Chip>
          {cuisines.map(c => (
            <Chip key={c} active={cuisine === c} onClick={() => setCuisine(c)}>{c}</Chip>
          ))}
        </div>
      </div>

      <div className="space-y-3">
        <h3 className="mt-0">How long have we got?</h3>
        <div className="flex flex-wrap gap-2">
          {TIMES.map(t => (
            <Chip key={t.label} active={maxTime === t.value} onClick={() => setMaxTime(t.value)}>
              {t.label}
            </Chip>
          ))}
        </div>
      </div>

      {nothing ? (
        <p className="text-center text-muted-foreground py-8">
          No recipes match. Try other filters.
        </p>
      ) : (
        <>
          {data.can_make.length > 0 && (
            <div>
              <h3>Ready to cook</h3>
              <ul className="grid sm:grid-cols-2 gap-3">
                {data.can_make.map(r => <RecipeCard key={r.id} recipe={r} onOpen={setOpenId} />)}
              </ul>
            </div>
          )}

          {data.missing_one.length > 0 && (
            <div>
              <h3>One ingredient away</h3>
              <ul className="grid sm:grid-cols-2 gap-3">
                {data.missing_one.map(r => (
                  <RecipeCard
                    key={r.id}
                    recipe={r}
                    onOpen={setOpenId}
                    note={<>Just add <strong>{r.missing_ingredient}</strong></>}
                  />
                ))}
              </ul>
            </div>
          )}
        </>
      )}
    </section>
  )
}
