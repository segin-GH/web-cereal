/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html"],
  theme: {
    extend: {
      colors: {
        'txt': '#c7c2c2',
        'bg1': '#181818',
        'bg2': '#171717',
        'bg3': '#1c1c1e',
        'pri': '#2a292a',
        'sec': '#020617',
        'acc': '#6366f1',
      },
      borderWidth: {
        'thin': '0.1px',
      },

    },
  },
  plugins: [
  ]
}
