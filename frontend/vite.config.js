import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  const apiUrl = env.VITE_API_URL || '';

  if (mode === 'production' && apiUrl.includes('your-render-service')) {
    throw new Error(
      'VITE_API_URL still uses the placeholder "your-render-service". ' +
        'Set it to your real Render URL in Vercel Environment Variables, e.g. ' +
        'https://resume-analyzer-api-23f3.onrender.com/api'
    );
  }

  return {
    plugins: [react()],
    server: {
      port: 5173,
      open: true,
    },
    build: {
      outDir: 'dist',
      sourcemap: false,
    },
  };
});
