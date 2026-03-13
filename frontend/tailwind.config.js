/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#0B1220',
        cyber: {
          bg: '#0F172A',
          panel: 'rgba(15, 23, 42, 0.55)',
          border: 'rgba(139, 92, 246, 0.35)',
          neonViolet: '#8B5CF6',
          neonPink: '#EC4899',
          neonCyan: '#22D3EE'
        }
      },
      boxShadow: {
        neon: '0 0 0 1px rgba(139,92,246,.35), 0 0 24px rgba(139,92,246,.25), 0 0 64px rgba(236,72,153,.15)',
        neonStrong: '0 0 0 1px rgba(236,72,153,.35), 0 0 28px rgba(236,72,153,.22), 0 0 90px rgba(34,211,238,.14)'
      },
      backgroundImage: {
        grid: 'linear-gradient(rgba(139,92,246,.10) 1px, transparent 1px), linear-gradient(90deg, rgba(236,72,153,.10) 1px, transparent 1px)',
        glow: 'radial-gradient(600px circle at var(--mx, 50%) var(--my, 30%), rgba(139,92,246,.25), transparent 40%), radial-gradient(500px circle at 30% 70%, rgba(236,72,153,.18), transparent 45%), radial-gradient(700px circle at 80% 20%, rgba(34,211,238,.14), transparent 50%)'
      },
      keyframes: {
        floaty: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-8px)' }
        },
        scan: {
          '0%': { transform: 'translateY(-30%)' },
          '100%': { transform: 'translateY(130%)' }
        },
        pulseGlow: {
          '0%, 100%': { opacity: '0.55' },
          '50%': { opacity: '1' }
        },
        shimmer: {
          '0%': { transform: 'translateX(-120%)' },
          '100%': { transform: 'translateX(120%)' }
        }
      },
      animation: {
        floaty: 'floaty 4.5s ease-in-out infinite',
        scan: 'scan 2.2s linear infinite',
        pulseGlow: 'pulseGlow 1.8s ease-in-out infinite',
        shimmer: 'shimmer 1.6s ease-in-out infinite'
      },
      borderRadius: {
        xl2: '1.25rem'
      }
    }
  },
  plugins: []
}
