<script setup lang="ts">
import { ref, computed } from 'vue';
import { useTheme } from 'vuetify';
import { useCustomizerStore } from '../../../stores/customizer';
import { SettingsIcon } from 'vue-tabler-icons';
import ProfileDD from './ProfileDD.vue';

const customizer = useCustomizerStore();
const theme = useTheme();
const showSearch = ref(false);

function searchbox() {
  showSearch.value = !showSearch.value;
}

const isDarkTheme = computed(() => theme.global.name.value === 'DarkTheme');

const toggleTheme = () => {
  const currentTheme = theme.global.name.value;
  theme.global.name.value = currentTheme === 'LightTheme' ? 'DarkTheme' : 'LightTheme';
};
</script>

<template>
  <v-app-bar elevation="0" height="80">
    <v-btn
      class="hidden-md-and-down text-secondary"
      color="lightsecondary"
      icon
      rounded="sm"
      variant="flat"
      @click.stop="customizer.SET_MINI_SIDEBAR(!customizer.mini_sidebar)"
      size="small"
    >
      <v-icon>
        {{ customizer.mini_sidebar ? 'mdi-chevron-right' : 'mdi-chevron-left' }}
      </v-icon>
    </v-btn>
    <v-btn
      class="hidden-lg-and-up text-secondary ms-3"
      color="lightsecondary"
      icon
      rounded="sm"
      variant="flat"
      @click.stop="customizer.SET_SIDEBAR_DRAWER"
      size="small"
    >
    </v-btn>

    <v-btn
      class="hidden-lg-and-up text-secondary ml-3"
      color="lightsecondary"
      icon
      rounded="sm"
      variant="flat"
      size="small"
      @click="searchbox"
    >
    </v-btn>

    <v-spacer />

    <div class="theme-switch-container mr-4">
      <div class="custom-theme-switch" @click="toggleTheme">
        <div class="switch-track" :class="{ 'track-active': isDarkTheme }">
          <v-icon class="track-icon sun-icon" size="16">mdi-white-balance-sunny</v-icon>
          <v-icon class="track-icon moon-icon" size="16">mdi-moon-waning-crescent</v-icon>
          <div class="switch-thumb" :class="{ 'thumb-active': isDarkTheme }"></div>
        </div>
      </div>
    </div>

    <v-menu :close-on-content-click="false">
      <template v-slot:activator="{ props }">
        <v-btn class="profileBtn text-primary" color="lightprimary" variant="flat" rounded="pill" v-bind="props">
          <v-avatar size="30">
            <v-icon size="30" class="mr-1">mdi-account</v-icon>
          </v-avatar>
          <SettingsIcon stroke-width="1.5" />
        </v-btn>
      </template>
      <v-sheet rounded="md" width="330" elevation="12">
        <ProfileDD />
      </v-sheet>
    </v-menu>
  </v-app-bar>
</template>

<style scoped>
.theme-switch-container {
  display: flex;
  align-items: center;
}

.custom-theme-switch {
  cursor: pointer;
}

.switch-track {
  position: relative;
  width: 60px;
  height: 32px;
  background: #e0e0e0;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 8px;
  transition: background-color 0.3s ease;
}

.track-icon {
  color: #757575;
  z-index: 1;
  transition: color 0.3s ease;
}

.sun-icon {
  color: white;
}

.moon-icon {
  color: #1cbc94;
}

.switch-thumb {
  position: absolute;
  width: 24px;
  height: 24px;
  background: white;
  border-radius: 50%;
  left: 4px;
  top: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease;
  z-index: 2;
}

.switch-thumb.thumb-active {
  transform: translateX(28px);
}

.switch-track.track-active {
  background: #1cbc94;
}
</style>
