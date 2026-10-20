/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        kid: {
          sky: '#E0F2FE',
          sun: '#FEF08A',
          grass: '#BBF7D0',
          orange: '#FFEDD5',
          pink: '#FCE7F3',
          purple: '#F3E8FF',
          coral: '#FF6B6B',
          teal: '#2DD4BF',
          primary: '#4F46E5',
          amber: '#F59E0B'
        }
      },
      fontFamily: {
        display: ['"Baloo 2"', 'system-ui', 'sans-serif'],
        sans: ['"Nunito"', 'system-ui', 'sans-serif']
      }
    },
  },
  plugins: [],
}
