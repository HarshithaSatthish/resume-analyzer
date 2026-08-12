import { useMemo } from 'react';
import { useTheme } from '../context/ThemeContext';
import { buildBaseOptions, getChartTheme } from '../utils/chartTheme';

export function useChartTheme() {
  const { isDark } = useTheme();

  return useMemo(
    () => ({
      isDark,
      theme: getChartTheme(isDark),
      baseOptions: (overrides = {}) => buildBaseOptions(isDark, overrides),
    }),
    [isDark]
  );
}
