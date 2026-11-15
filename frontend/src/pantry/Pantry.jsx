import { useEffect, useState } from 'react'
import { api } from '../api'

export default function Pantry({ onChange }) {
  const [items, setItems] = useState([])
  const [ingredient, setIngredient] = useState('')
  const [quantity, setQuantity] = useState('')
  const [unit, setUnit] = useState('g')
  const [error, setError] = useState('')

  async function load() {
    setItems(await api('/pantry'))
    onChange()
  }

  useEffect(() => { api('/pantry').then(setItems) }, [])

  async function addItem(e) {
    e.preventDefault()
    setError('')
    try {
      await api('/pantry', {
        method: 'POST',
        body: { ingredient, quantity: Number(quantity), unit },
      })
      setIngredient('')
      setQuantity('')
      load()
    } catch (err) {
      setError(err.message)
    }
  }

  async function deleteItem(id) {
    await api(`/pantry/${id}`, { method: 'DELETE' })
    load()
  }

  return (
    <section>
      <h2>My pantry</h2>

      <form onSubmit={addItem}>
        <input placeholder="Ingredient" value={ingredient} onChange={e => setIngredient(e.target.value)} />
        <input type="number" placeholder="Qty" value={quantity} onChange={e => setQuantity(e.target.value)} />
        <input placeholder="Unit" value={unit} onChange={e => setUnit(e.target.value)} />
        <button type="submit">Add</button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {items.length === 0 ? <p>Your pantry is empty.</p> : (
        <ul>
          {items.map(item => (
            <li key={item.id}>
              {item.ingredient_name} — {item.quantity} {item.unit}
              <button onClick={() => deleteItem(item.id)}>Delete</button>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}