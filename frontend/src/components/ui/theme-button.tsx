'use client';

import { cn } from '@/lib/utils';
import { MoonIcon, SunIcon } from '@radix-ui/react-icons';
import { useTheme } from 'next-themes';
import { useEffect, useState } from 'react';
import { Button } from './button';

const THEME = {
  DARK: 'dark',
  LIGHT: 'light',
};

export interface ThemeButtonProps {
  className?: string;
}

export function ThemeButton({ className }: ThemeButtonProps) {
  const { setTheme, systemTheme, theme } = useTheme();
  const [selectedTheme, setSelectedTheme] = useState<string>(
    systemTheme ?? 'light'
  );

  useEffect(() => {
    if (theme) {
      setSelectedTheme(theme);
    }
  }, [theme]);

  const changeThemeHandler = () => {
    switch (theme ?? systemTheme) {
      case THEME.LIGHT:
        setTheme(THEME.DARK);
        break;

      case THEME.LIGHT:
        setTheme(THEME.DARK);
        break;

      default:
        setTheme(THEME.LIGHT);
        break;
    }
  };

  return (
    <Button
      className={cn('text-2xl mx-4 mb-2 mt-4 p-0', className)}
      onClick={changeThemeHandler}
    >
      {selectedTheme === THEME.LIGHT ? (
        <MoonIcon className="h-6 w-6" />
      ) : (
        <SunIcon className="h-6 w-6" />
      )}
    </Button>
  );
}
