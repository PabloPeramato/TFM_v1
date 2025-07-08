import { createVuetify } from 'vuetify';
import '@mdi/font/css/materialdesignicons.css';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import { LightTheme } from '@/theme/LightTheme';
import { DarkTheme } from '@/theme/DarkTheme';

export default createVuetify({
  components,
  directives,

  theme: {
    defaultTheme: 'LightTheme',
    themes: {
      LightTheme,
      DarkTheme
    }
  },
  defaults: {
    VBtn: {},
    VCard: {
      rounded: 'md'
    },
    VTextField: {
      rounded: 'lg'
    },
    VTooltip: {
      // set v-tooltip default location to top
      location: 'top'
    }
  }
});
