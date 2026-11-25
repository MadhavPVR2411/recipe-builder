import { useEffect, useState } from 'react'
import { api } from '../api'
import RecipeDetail from './RecipeDetail'

export default function Recipes() {
  const [recipes, setRecipes] = useState([])
  const [diet, setDiet] = useState('')
  const [selectedId, setSelectedId] = useState(null)

  useEffect(() => {
    const url = diet ? `/recipes?diet_type=${diet}` : '/recipes'
    api(url).then(setRecipes)
  }, [diet])

  if (selectedId) {
    return (
      <RecipeDetail
        recipeId={selectedId}
        onBack={() => setSelectedId(null)}
        backLabel="Back to recipes"
      />
    )
  }

  return (
    <section className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 className="mb-0">All recipes</h2>
        <select value={diet} onChange={e => setDiet(e.target.value)}>
          <option value="">All diets</option>
          <option value="veg">Veg</option>
          <option value="egg">Egg</option>
          <option value="non_veg">Non-veg</option>
        </select>
      </div>

      <ul className="divide-y border rounded-xl overflow-hidden">
        {recipes.map(r => (
          <li key={r.id}>
            <button
              type="button"
              onClick={() => setSelectedId(r.id)}
              className="w-full flex items-center gap-3 text-left bg-card text-foreground rounded-none px-4 py-3 font-normal hover:bg-background"
            >
              <span className="flex-1 font-medium">{r.name}</span>
              <span className="text-sm text-muted-foreground">
                {r.cuisine} | {r.total_time} min | {r.complexity}
              </span>
            </button>
          </li>
        ))}
      </ul>
    </section>
  )
}
