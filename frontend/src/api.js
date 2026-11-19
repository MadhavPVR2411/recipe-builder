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

  const text = await res.text()
  let data = null
  try {
    data = text ? JSON.parse(text) : null
  } catch {
    // not JSON, e.g. a plain-text 500
  }

  if (!res.ok) {
    const detail = data?.detail
    const message = Array.isArray(detail)
      ? detail.map(d => d.msg).join(', ')
      : detail ?? (text || 'Request failed')
    throw new Error(message)
  }
  return data
}