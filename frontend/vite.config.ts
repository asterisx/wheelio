import { defineConfig } from "vitest/config"
import react from "@vitejs/plugin-react"
import dotenv from "dotenv"

dotenv.config()

export default defineConfig({
  plugins: [react()],
  define: {
    VITE_BACKEND_URL: process.env.BACKEND_URL,
  },
  server: {
    open: true,
  },
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: "src/setupTests",
    mockReset: true,
  },
})
