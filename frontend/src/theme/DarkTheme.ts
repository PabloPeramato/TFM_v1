import type { ThemeTypes } from '@/types/themeTypes/ThemeType';

const DarkTheme: ThemeTypes = {
  name: 'DarkTheme',
  dark: true,
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
    
    lightprimary: '#0f3d32',
    lightsecondary: '#0f3d32',
    lightsuccess: '#1b3b1f',
    lighterror: '#3f1a1a',
    lightwarning: '#3f3517',
    
    darkText: '#ffffff',
    lightText: '#b0b0b0',
    
    darkprimary: '#16A085',
    darksecondary: '#4527a0',
    
    borderLight: '#404040',
    inputBorder: '#606060',
    containerBg: '#1a1a1a',  
    surface: '#2a2a2a',     
    'on-surface-variant': '#2a2a2a',
    
    facebook: '#4267b2',
    twitter: '#1da1f2',
    linkedin: '#0e76a8',
    
    gray100: '#1e1e1e',
    primary200: '#16A085',
    secondary200: '#6b46c1'
  }
};

export { DarkTheme };