import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  
  // Ensures correct paths for static assets
  base: "/",

  build: {
    outDir: "/var/www/bill-easy-frontend",  // Nginx serving folder
    emptyOutDir: true,                      // Clean old files before build
    sourcemap: true,                        // Enable readable error messages
    rollupOptions: {
      input: path.resolve(__dirname, "index.html"), // Entry point
    },
  },

  server: {
    port: 5173,
    open: true,
    proxy: {
      "/api": {
        target: "http://localhost:8000", // Backend service
        changeOrigin: true,
        secure: false,
      },
    },
  },
});

