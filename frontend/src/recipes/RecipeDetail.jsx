import { useEffect, useState } from 'react'
import { api } from '../api'

export default function RecipeDetail({ recipeId, onBack, backLabel = 'Back' }) {
  const [detail, setDetail] = useState(null)

  useEffect(() => {
    api(`/recipes/${recipeId}`).then(setDetail)
  }, [recipeId])

  if (detail?.id !== recipeId) {
    return <p className="text-muted-foreground">Loading recipe</p>
  }

  const checked = detail.ingredients.some(i => i.in_pantry !== null)
  const haveCount = checked ? detail.ingredients.filter(i => i.in_pantry).length : null

  return (
    <section>
      <button type="button" onClick={onBack} className="mb-4">{backLabel}</button>
      <h2>{detail.name}</h2>
      <p>{detail.cuisine} | {detail.diet_type} | {detail.complexity} | serves {detail.serving}</p>
      <p>Prep {detail.prep_time} min | Cook {detail.cook_time} min</p>

      <h3>Ingredients</h3>
      {haveCount !== null && (
        <p className="text-sm text-muted-foreground mb-2">
          You have {haveCount} of {detail.ingredients.length}
        </p>
      )}
      <ul className="divide-y border rounded-xl overflow-hidden">
        {detail.ingredients.map(i => (
          <li key={i.name} className="flex items-center gap-3 px-4 py-2 bg-card">
            <span className="flex-1 capitalize">{i.name}</span>
            <span className="text-muted-foreground tabular-nums">{i.quantity} {i.unit}</span>
            {i.in_pantry === false && (
              <span className="text-xs font-semibold text-destructive bg-destructive/10 rounded-full px-2 py-0.5">
                missing
              </span>
            )}
          </li>
        ))}
      </ul>

      <h3>Steps</h3>
      <ol>
        {detail.steps.map((step, n) => <li key={n}>{step}</li>)}
      </ol>
    </section>
  )
}
