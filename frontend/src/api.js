export async function api(path, { method = 'GET', body } = {}) {
  const headers = { 'Content-Type': 'application/json' }
  const token = localStorage.getItem('token')
  if (token) headers.Authorization = `Bearer ${token}`

  const res = await fetch(path, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  })

  // expired token, send back to login
  if (res.status === 401 && token) {
    localStorage.removeItem('token')
    window.location.reload()
    return new Promise(() => {})
  }

  if (res.status === 204) return null
  const data = await res.json()
  if (!res.ok) throw new Error(data.detail ?? 'Request failed')
  return data
}