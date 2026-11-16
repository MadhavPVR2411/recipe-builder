import { useEffect, useState } from 'react'
import { api } from '../api'

export default function Recipes() {
  const [recipes, setRecipes] = useState([])
  const [diet, setDiet] = useState('')
  const [selectedId, setSelectedId] = useState(null)
  const [detail, setDetail] = useState(null)

  useEffect(() => {
    const url = diet ? `/recipes?diet_type=${diet}` : '/recipes'
    api(url).then(setRecipes)
  }, [diet])

  useEffect(() => {
    if (selectedId) api(`/recipes/${selectedId}`).then(setDetail)
  }, [selectedId])

  if (selectedId && detail?.id === selectedId) {
    return (
      <section>
        <button onClick={() => setSelectedId(null)}>Back to recipes</button>
        <h2>{detail.name}</h2>
        <p>{detail.cuisine} | {detail.diet_type} | {detail.complexity} | serves {detail.serving}</p>
        <p>Prep {detail.prep_time} min | Cook {detail.cook_time} min</p>

        <h3>Ingredients</h3>
        <ul>
          {detail.ingredients.map(i => (
            <li key={i.name}>{i.quantity} {i.unit} {i.name}</li>
          ))}
        </ul>

        <h3>Steps</h3>
        <ol>
          {detail.steps.map((step, n) => <li key={n}>{step}</li>)}
        </ol>
      </section>
    )
  }

  return (
    <section>
      <h2>All recipes</h2>
      <select value={diet} onChange={e => setDiet(e.target.value)}>
        <option value="">All diets</option>
        <option value="veg">Veg</option>
        <option value="egg">Egg</option>
        <option value="non_veg">Non-veg</option>
      </select>

      <ul>
        {recipes.map(r => (
          <li key={r.id}>
            <button onClick={() => setSelectedId(r.id)}>{r.name}</button>
            {' '}{r.cuisine} | {r.total_time} min | {r.complexity}
          </li>
        ))}
      </ul>
    </section>
  )
}