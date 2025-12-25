/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#8B5CF6',
        secondary: '#FF8C00',
        accent: '#10B981',
        cream: '#FFFBF5',
      },
    },
  },
  plugins: [],
}
