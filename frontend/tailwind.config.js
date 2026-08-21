/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: '#E85D38',
          light: '#FCEFE9',
        },
        surface: {
          DEFAULT: '#F9FAFB',
          panel: '#FFFFFF',
        },
        ink: {
          DEFAULT: '#111827',
          dim: '#4B5563',
          muted: '#9CA3AF',
        }
      }
    },
  },
  plugins: [],
}