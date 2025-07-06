<script setup lang="ts">
import { SettingsIcon, LogoutIcon, UserIcon } from 'vue-tabler-icons';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
</script>

<template>
  <!-- ---------------------------------------------- -->
  <!-- profile DD -->
  <!-- ---------------------------------------------- -->
  <div class="pa-4">
    <h4 class="mb-2">Usuario</h4>

    <perfect-scrollbar style="height: calc(100vh - 300px); max-height: 315px">
      <v-divider></v-divider>

      <v-list class="mt-3">
        <v-list-item color="secondary" rounded="md">
          <template v-slot:prepend>
            <SettingsIcon size="20" class="mr-2" />
          </template>

          <v-list-item-title class="text-subtitle-2"> Ajustes </v-list-item-title>
        </v-list-item>

        <v-list-item color="secondary" rounded="md">
          <template v-slot:prepend>
            <UserIcon size="20" class="mr-2" />
          </template>

          <v-list-item-title class="text-subtitle-2"> Gestión de usuarios </v-list-item-title>
        </v-list-item>

        <v-list-item @click="authStore.logout()" color="secondary" rounded="md">
          <template v-slot:prepend>
            <LogoutIcon size="20" class="mr-2" />
          </template>

          <v-list-item-title class="text-subtitle-2"> Cerrar sesión</v-list-item-title>
        </v-list-item>
      </v-list>
    </perfect-scrollbar>
  </div>
</template>
