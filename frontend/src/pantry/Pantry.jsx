import {useEffect, useState} from 'react'
import {api} from '../api'

export default function Pantry() {
    const [items, setItems] = useState([])
    const [ingredient, setIngredient] = useState('')
    const [quantity, setQuantity] = useState('')
    const [error, setError] = useState('')
    const [options, setOptions] = useState([])
    const [unit, setUnit] = useState('')
    async function load() {
        setItems(await api('/pantry'))
    }

    useEffect(() => {
        api('/pantry').then(setItems)
    }, [])
    useEffect(() => {
        api('/pantry/ingredients').then(setOptions)
    }, [])

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
        } catch (err) {
            setError(err.message)
        }
    }

    async function deleteItem(id) {
        await api(`/pantry/${id}`, {method: 'DELETE'})
        load()
    }

    const selected = options.find(o => o.name === ingredient)

    function pickIngredient(name) {
        setIngredient(name)
        const option = options.find(o => o.name === name)
        setUnit(option ? option.units[0] : '')
    }

    return (
        <section>
            <h2>My pantry</h2>

            <form onSubmit={addItem}>
                <select value={ingredient} onChange={e => pickIngredient(e.target.value)}>
                    <option value="">Choose an ingredient</option>
                    {options.map(o => <option key={o.id} value={o.name}>{o.name}</option>)}
                </select>

                <input type="number" placeholder="Qty" value={quantity} onChange={e => setQuantity(e.target.value)}/>

                <select value={unit} onChange={e => setUnit(e.target.value)} disabled={!selected}>
                    {selected?.units.map(u => <option key={u} value={u}>{u}</option>)}
                </select>

                <button type="submit">Add</button>
            </form>
            {error && <p style={{color: 'red'}}>{error}</p>}

            {items.length === 0 ? <p>Your pantry is empty.</p> : (
                <ul>
                    {items.map(item => (
                        <li key={item.id}>
                            {item.ingredient_name}: {item.quantity} {item.unit}
                            <button onClick={() => deleteItem(item.id)}>Delete</button>
                        </li>
                    ))}
                </ul>
            )}
        </section>
    )
}