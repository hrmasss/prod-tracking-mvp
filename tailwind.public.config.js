import defaultTheme from "tailwindcss/defaultTheme";

module.exports = {
    darkMode: "class",
    content: {
        relative: true,
        transform: (content) => content.replace(/taos:/g, ""),
        files: [
            "./node_modules/preline/preline.js",
            "./templates/**/*.{html,js,py}",
            "!./templates/admin/**/*.{html,js,py}",
            "./common/**/*.{html,js}",
            "./users/**/*.{html,js}",
        ],
    },
    theme: {
        extend: {
            colors: {
                foreground: "hsl(var(--foreground))",
                background: "hsl(var(--background))",
                card: "hsl(var(--card))",
                border: "hsl(var(--border))",
                primary: "hsl(var(--primary))",
                accent: "hsl(var(--accent))",
            },
            fontFamily: {
                sans: ["Chivo", ...defaultTheme.fontFamily.sans],
            },
        },
    },
    darkMode: "class",
    plugins: [
        require("@tailwindcss/typography"),
        require("@tailwindcss/forms"),
        require("preline/plugin"),
    ],
};
