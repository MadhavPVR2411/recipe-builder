import { useEffect, useState } from 'react'
import { api } from '../api'

export default function Suggestions({ version }) {
  const [data, setData] = useState({ can_make: [], missing_one: [] })

  useEffect(() => { api('/suggestions').then(setData) }, [version])

  return (
    <section>
      <h2>What can I cook?</h2>

      <h3>You can make</h3>
      {data.can_make.length === 0 ? <p>Nothing yet. Add more to your pantry.</p> : (
        <ul>
          {data.can_make.map(r => (
            <li key={r.id}>{r.name} · {r.cuisine} · {r.total_time} min · {r.complexity}</li>
          ))}
        </ul>
      )}

      <h3>Missing just one ingredient</h3>
      {data.missing_one.length === 0 ? <p>None.</p> : (
        <ul>
          {data.missing_one.map(r => (
            <li key={r.id}>{r.name}: add <strong>{r.missing_ingredient}</strong></li>
          ))}
        </ul>
      )}
    </section>
  )
}