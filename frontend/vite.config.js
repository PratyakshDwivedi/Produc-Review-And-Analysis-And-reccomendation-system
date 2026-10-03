import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// Proxy API calls to the FastAPI backend during development.
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://127.0.0.1:8000',
      '/health': 'http://127.0.0.1:8000',
    },
  },
})
