<script setup lang="ts">
import { LogoutIcon, UserIcon } from 'vue-tabler-icons';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

function goToProfile() {
  router.push('/profile');
}
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
        <v-list-item @click="goToProfile" rounded="md" class="clickable-item" :ripple="false">
          <template v-slot:prepend>
            <UserIcon size="20" class="mr-2" />
          </template>
          <v-list-item-title class="text-subtitle-2"> Mi perfil </v-list-item-title>
        </v-list-item>

        <v-list-item @click="authStore.logout()" rounded="md" class="clickable-item" :ripple="false">
          <template v-slot:prepend>
            <LogoutIcon size="20" class="mr-2" />
          </template>
          <v-list-item-title class="text-subtitle-2"> Cerrar sesión</v-list-item-title>
        </v-list-item>
      </v-list>
    </perfect-scrollbar>
  </div>
</template>

<style scoped>
.clickable-item {
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.clickable-item:hover {
  background-color: rgba(28, 188, 148, 0.08) !important;
}

.clickable-item:active {
  background-color: rgba(28, 188, 148, 0.2) !important;
  transform: scale(0.98);
}
</style>
