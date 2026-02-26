/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './templates/**/*.html',
    './apps/**/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',
        secondary: '#10B981',
        danger: '#EF4444',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
