import type { ThemeTypes } from '@/types/themeTypes/ThemeType';

const LightTheme: ThemeTypes = {
  name: 'LightTheme',
  dark: false,
  variables: {
    'border-color': '#1CBC94',
    'carousel-control-size': 10
  },
  colors: {
    primary: '#1CBC94',
    secondary: '#1CBC94',
    info: '#03c9d7',
    success: '#00c853',
    accent: '#FFAB91',
    warning: '#ffc107',
    error: '#f44336',
    lightprimary: '#c5e5dd',
    lightsecondary: '#c5e5dd',
    lightsuccess: '#b9f6ca',
    lighterror: '#f9d8d8',
    lightwarning: '#fff8e1',
    darkText: '#212121',
    lightText: '#616161',
    darkprimary: '#1565c0',
    darksecondary: '#4527a0',
    borderLight: '#d0d0d0',
    inputBorder: '#787878',
    containerBg: '#eef2f6',
    surface: '#fff',
    'on-surface-variant': '#fff',
    facebook: '#4267b2',
    twitter: '#1da1f2',
    linkedin: '#0e76a8',
    gray100: '#fafafa',
    primary200: '#90caf9',
    secondary200: '#b39ddb'
  }
};

export { LightTheme };
