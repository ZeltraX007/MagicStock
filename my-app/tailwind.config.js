/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#1e40af',   // primary
          dark: '#1e3a8a',      // primary-dark
          light: '#3b82f6',     // primary-light
        },
        secondary: {
          DEFAULT: '#f59e0b',
          dark: '#b45309',
          light: '#fbbf24',
        },
        neutral: {
          light: '#f5f5f5',
          DEFAULT: '#e5e7eb',
          dark: '#374151',
        },
        accent: '#10b981', // emerald
      },
    },
  },
  plugins: [],
};