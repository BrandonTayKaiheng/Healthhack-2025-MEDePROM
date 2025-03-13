/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        "dark-blue": "#022E6B",
        "light-grey": "#F6F6F7",
        "orange": "#E36F04",
      },
    },
  },
  plugins: [],
};
