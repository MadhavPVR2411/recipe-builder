import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/auth': 'http://localhost:8000',
      '/profile': 'http://localhost:8000',
      '/allergens': 'http://localhost:8000',
      '/recipes': 'http://localhost:8000',
      '/pantry': 'http://localhost:8000',
      '/suggestions': 'http://localhost:8000',
    },
  },
})