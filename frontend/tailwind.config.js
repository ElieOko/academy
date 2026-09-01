/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts}'],
  theme: {
    extend: {
      colors: {
        navy: {
          DEFAULT: '#0B1F36',
          50: '#F3F6F9',
          100: '#E4EBF3',
          700: '#16324F',
          800: '#10253D',
          900: '#0B1F36',
        },
        gold: {
          DEFAULT: '#C4A35A',
          light: '#E8D5A3',
          dark: '#9A7A32',
        },
        wine: {
          DEFAULT: '#922B3E',
          light: '#B23A51',
          dark: '#721F30',
        },
        cream: '#F6F3EE',
        ink: '#14181F',
        mute: '#5C6570',
      },
      fontFamily: {
        display: ['Fraunces', 'Georgia', 'serif'],
        sans: ['Outfit', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        soft: '0 18px 50px -24px rgba(11, 31, 54, 0.35)',
      },
    },
  },
  plugins: [],
}
