import { useEffect, useRef, useState } from 'react'
import { api } from '../api'

// show big amounts in the larger unit, e.g. 1700 g -> 1.7 kg
function formatAmount(quantity, unit) {
  if (unit === 'g' && quantity >= 1000) return `${quantity / 1000} kg`
  if (unit === 'ml' && quantity >= 1000) return `${quantity / 1000} litre`
  return `${quantity} ${unit}`
}

// sensible starting amount for each unit, so the quantity box is pre-filled
const DEFAULT_AMOUNT = {pcs: 1, g: 100, kg: 1, ml: 100, litre: 1}

// common ingredients offered as one-click buttons
const STAPLES = ['salt', 'olive oil', 'onion', 'garlic', 'tomato', 'potato', 'rice', 'egg', 'milk', 'butter', 'flour', 'sugar']

function formatDate(value) {
  return new Date(value).toLocaleDateString('en-GB', {day: 'numeric', month: 'short'})
}

export default function Pantry() {
  const [items, setItems] = useState([])
  const [options, setOptions] = useState([])
  const [ingredient, setIngredient] = useState('')
  const [quantity, setQuantity] = useState('')
  const [unit, setUnit] = useState('')
  const [error, setError] = useState('')
  const ingredientInput = useRef(null)

  async function load() {
    setItems(await api('/pantry'))
  }

  useEffect(() => {
    api('/pantry').then(setItems)
  }, [])
  useEffect(() => {
    api('/pantry/ingredients').then(setOptions)
  }, [])

  const selected = options.find(o => o.name === ingredient.trim().toLowerCase())
  const inPantry = new Set(items.map(i => i.ingredient_name))
  const staples = STAPLES
    .map(name => options.find(o => o.name === name))
    .filter(o => o && !inPantry.has(o.name))
  const sorted = [...items].sort((a, b) => a.ingredient_name.localeCompare(b.ingredient_name))

  function pickIngredient(name) {
    setIngredient(name)
    const option = options.find(o => o.name === name.trim().toLowerCase())
    setUnit(option ? option.units[0] : '')
    if (option && quantity === '') setQuantity(String(DEFAULT_AMOUNT[option.units[0]]))
  }

  async function quickAdd(option) {
    setError('')
    const unit = option.units[0]
    try {
      await api('/pantry', {
        method: 'POST',
        body: {ingredient: option.name, quantity: DEFAULT_AMOUNT[unit], unit},
      })
      load()
    } catch (err) {
      setError(err.message)
    }
  }

  async function addItem(e) {
    e.preventDefault()
    setError('')
    try {
      await api('/pantry', {
        method: 'POST',
        body: {ingredient, quantity: Number(quantity), unit},
      })
      setIngredient('')
      setQuantity('')
      setUnit('')
      load()
      ingredientInput.current?.focus()
    } catch (err) {
      setError(err.message)
    }
  }

  async function deleteItem(id) {
    await api(`/pantry/${id}`, {method: 'DELETE'})
    load()
  }

  return (
    <section className="space-y-5">
      <div className="flex items-baseline justify-between">
        <h2 className="mb-0">My pantry</h2>
        <span className="text-sm text-muted-foreground">
          {items.length} {items.length === 1 ? 'item' : 'items'}
        </span>
      </div>

      <form onSubmit={addItem} className="flex flex-wrap gap-2 bg-background rounded-xl p-3 border">
        <input
          ref={ingredientInput}
          list="ingredient-options"
          placeholder="Type an ingredient"
          value={ingredient}
          onChange={e => pickIngredient(e.target.value)}
          className="flex-1 min-w-48"
          autoFocus
        />
        <datalist id="ingredient-options">
          {options.map(o => <option key={o.id} value={o.name} />)}
        </datalist>

        <input
          type="number"
          min="0"
          step="any"
          placeholder="Qty"
          value={quantity}
          onChange={e => setQuantity(e.target.value)}
          className="w-24"
        />

        <select
          value={unit}
          onChange={e => setUnit(e.target.value)}
          disabled={!selected}
          className="w-24"
        >
          {selected?.units.map(u => <option key={u} value={u}>{u}</option>)}
        </select>

        <button type="submit" disabled={!selected || !quantity}>Add</button>
      </form>

      {staples.length > 0 && (
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-sm text-muted-foreground mr-1">Quick add:</span>
          {staples.map(o => (
            <button
              key={o.id}
              type="button"
              onClick={() => quickAdd(o)}
              className="bg-card text-primary border rounded-full px-3 py-1 text-sm capitalize"
            >
              + {o.name}
            </button>
          ))}
        </div>
      )}
      {error && <p className="text-sm text-destructive">{error}</p>}

      {sorted.length === 0 ? (
        <p className="text-center text-muted-foreground py-8">
          Your pantry is empty. Add what you have at home to see what you can cook.
        </p>
      ) : (
        <ul className="divide-y border rounded-xl overflow-hidden">
          {sorted.map(item => (
            <li key={item.id} className="flex items-center gap-4 px-4 py-3 bg-card">
              <span className="flex-1 font-medium capitalize">{item.ingredient_name}</span>
              {item.expiry_date && (
                <span className="text-xs text-muted-foreground">
                  use by {formatDate(item.expiry_date)}
                </span>
              )}
              <span className="w-24 text-right tabular-nums text-muted-foreground">
                {formatAmount(item.quantity, item.unit)}
              </span>
              <button
                type="button"
                onClick={() => deleteItem(item.id)}
                aria-label={`Remove ${item.ingredient_name}`}
                className="bg-transparent text-muted-foreground px-2 py-1 text-sm hover:text-destructive hover:bg-destructive/10"
              >
                Remove
              </button>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
