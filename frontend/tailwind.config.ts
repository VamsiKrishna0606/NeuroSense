import type { Config } from "tailwindcss";

export default {
  darkMode: ["class"],
  content: ["./pages/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./app/**/*.{ts,tsx}", "./src/**/*.{ts,tsx}"],
  prefix: "",
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      fontFamily: {
        display: ['Orbitron', 'sans-serif'],
        body: ['Rajdhani', 'sans-serif'],
      },
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        sidebar: {
          DEFAULT: "hsl(var(--sidebar-background))",
          foreground: "hsl(var(--sidebar-foreground))",
          primary: "hsl(var(--sidebar-primary))",
          "primary-foreground": "hsl(var(--sidebar-primary-foreground))",
          accent: "hsl(var(--sidebar-accent))",
          "accent-foreground": "hsl(var(--sidebar-accent-foreground))",
          border: "hsl(var(--sidebar-border))",
          ring: "hsl(var(--sidebar-ring))",
        },
        // Solo Leveling Custom Colors
        glow: {
          cyan: "hsl(var(--glow-cyan))",
          blue: "hsl(var(--glow-blue))",
          purple: "hsl(var(--glow-purple))",
          pink: "hsl(var(--glow-pink))",
        },
        void: {
          deep: "hsl(var(--void-deep))",
        },
        glass: {
          DEFAULT: "hsl(var(--glass))",
          border: "hsl(var(--glass-border))",
        },
        band: {
          theta: "hsl(var(--theta))",
          alpha: "hsl(var(--alpha))",
          beta: "hsl(var(--beta))",
          gamma: "hsl(var(--gamma))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
        "pulse-glow": {
          "0%, 100%": { 
            opacity: "0.6",
            transform: "scale(1)",
          },
          "50%": { 
            opacity: "1",
            transform: "scale(1.05)",
          },
        },
        "float": {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-20px)" },
        },
        "spin-slow": {
          from: { transform: "rotate(0deg)" },
          to: { transform: "rotate(360deg)" },
        },
        "brain-pulse": {
          "0%, 100%": { 
            filter: "drop-shadow(0 0 20px hsl(var(--glow-cyan) / 0.5))",
            opacity: "0.8",
          },
          "50%": { 
            filter: "drop-shadow(0 0 40px hsl(var(--glow-cyan) / 0.8))",
            opacity: "1",
          },
        },
        "data-flow": {
          "0%": { 
            backgroundPosition: "0% 50%",
            opacity: "0.5",
          },
          "50%": { 
            backgroundPosition: "100% 50%",
            opacity: "1",
          },
          "100%": { 
            backgroundPosition: "0% 50%",
            opacity: "0.5",
          },
        },
        "scan-line": {
          "0%": { transform: "translateY(-100%)" },
          "100%": { transform: "translateY(100%)" },
        },
        "shimmer": {
          "0%": { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
        "gauge-fill": {
          from: { strokeDashoffset: "283" },
          to: { strokeDashoffset: "var(--gauge-value)" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        "pulse-glow": "pulse-glow 2s ease-in-out infinite",
        "float": "float 6s ease-in-out infinite",
        "spin-slow": "spin-slow 20s linear infinite",
        "brain-pulse": "brain-pulse 3s ease-in-out infinite",
        "data-flow": "data-flow 3s ease infinite",
        "scan-line": "scan-line 3s linear infinite",
        "shimmer": "shimmer 2s linear infinite",
        "gauge-fill": "gauge-fill 1.5s ease-out forwards",
      },
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic": "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
        "cyber-grid": `
          linear-gradient(hsl(var(--primary) / 0.03) 1px, transparent 1px),
          linear-gradient(90deg, hsl(var(--primary) / 0.03) 1px, transparent 1px)
        `,
      },
      backgroundSize: {
        "cyber-grid": "50px 50px",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
} satisfies Config;
