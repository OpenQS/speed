import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  // tell Vite to prefix all asset URLs with '/speed/'
  base: '/speed/',
  plugins: [react()],
  build: {
    outDir: 'docs'
  }
})