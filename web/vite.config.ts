import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

// GitHub Pages project site: https://<user>.github.io/agama-kumarajiva/
const base =
  process.env.GITHUB_PAGES === "true" ? "/agama-kumarajiva/" : "/";

export default defineConfig({
  base,
  plugins: [react(), tailwindcss()],
  server: { port: 5173 },
});
