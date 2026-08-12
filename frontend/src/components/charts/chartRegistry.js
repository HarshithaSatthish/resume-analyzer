import {
  ArcElement,
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Filler,
  Legend,
  LineElement,
  LinearScale,
  PointElement,
  Title,
  Tooltip,
} from 'chart.js';

let isRegistered = false;

export function registerCharts() {
  if (isRegistered) return;
  ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    ArcElement,
    Title,
    Tooltip,
    Legend,
    Filler
  );
  ChartJS.defaults.font.family = 'Inter, system-ui, sans-serif';
  ChartJS.defaults.color = '#64748b';
  isRegistered = true;
}

registerCharts();
