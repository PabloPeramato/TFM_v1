<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';
import BaseBreadcrumb from '@/components/shared/BaseBreadcrumb.vue';
import UiParentCard from '@/components/shared/UiParentCard.vue';

const authStore = useAuthStore();
const router = useRouter();

const page = ref({ title: 'My Profile' });
const breadcrumbs = ref([
  { title: 'Profile', disabled: true, href: '#' }
]);

// Datos del perfil
const profileData = ref({
  username: authStore.user?.username || '',
  email: authStore.user?.email || '',
  firstName: '',
  lastName: '',
  phone: '',
  location: '',
  bio: ''
});

// Estados de edición
const isEditingProfile = ref(false);
const isEditingPassword = ref(false);
const isLoading = ref(false);
const successMessage = ref('');
const errorMessage = ref('');

// Datos de cambio de contraseña
const passwordData = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
});

// Funciones
function editProfile() {
  isEditingProfile.value = true;
  errorMessage.value = '';
  successMessage.value = '';
}

function cancelEditProfile() {
  isEditingProfile.value = false;
  // Restaurar datos originales
  profileData.value = {
    username: authStore.user?.username || '',
    email: authStore.user?.email || '',
    firstName: '',
    lastName: '',
    phone: '',
    location: '',
    bio: ''
  };
}

async function saveProfile() {
  isLoading.value = true;
  errorMessage.value = '';
  
  try {
    // Aquí iría la llamada a la API para actualizar el perfil
    // await authStore.updateProfile(profileData.value);
    
    // Simulación de guardado exitoso
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    successMessage.value = 'Perfil actualizado correctamente';
    isEditingProfile.value = false;
  } catch (error) {
    errorMessage.value = 'Error al actualizar el perfil';
    console.error('Error updating profile:', error);
  } finally {
    isLoading.value = false;
  }
}

function editPassword() {
  isEditingPassword.value = true;
  errorMessage.value = '';
  successMessage.value = '';
  passwordData.value = {
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  };
}

function cancelEditPassword() {
  isEditingPassword.value = false;
  passwordData.value = {
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  };
}

async function savePassword() {
  if (passwordData.value.newPassword !== passwordData.value.confirmPassword) {
    errorMessage.value = 'Las contraseñas no coinciden';
    return;
  }
  
  if (passwordData.value.newPassword.length < 6) {
    errorMessage.value = 'La contraseña debe tener al menos 6 caracteres';
    return;
  }

  isLoading.value = true;
  errorMessage.value = '';
  
  try {
    // Aquí iría la llamada a la API para cambiar contraseña
    // await authStore.changePassword(passwordData.value);
    
    // Simulación de cambio exitoso
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    successMessage.value = 'Contraseña actualizada correctamente';
    isEditingPassword.value = false;
  } catch (error) {
    errorMessage.value = 'Error al cambiar la contraseña';
    console.error('Error changing password:', error);
  } finally {
    isLoading.value = false;
  }
}

async function logout() {
  try {
    await authStore.logout();
    router.push('/login');
  } catch (error) {
    console.error('Error logging out:', error);
  }
}

onMounted(() => {
  // Cargar datos adicionales del perfil si es necesario
});
</script>

<template>
  <BaseBreadcrumb :title="page.title" :breadcrumbs="breadcrumbs" />

  <v-row>
    <v-col cols="12" lg="4">
      <!-- Card de información básica -->
      <UiParentCard>
        <template #title>
          <span style="color: #1CBC94">Información Personal</span>
        </template>

        <div class="text-center mb-6">
          <v-avatar size="100" color="#1CBC94">
            <span class="text-h4 text-white">
              {{ profileData.username.charAt(0).toUpperCase() }}
            </span>
          </v-avatar>
          <h3 class="text-h5 font-weight-bold mt-4">{{ profileData.username }}</h3>
          <p class="text-subtitle-1 text-grey">{{ profileData.email }}</p>
        </div>

        <v-divider class="mb-4" />

        <div class="mb-4">
          <v-chip color="#1CBC94" variant="flat" size="small" class="mb-2">
            Usuario activo
          </v-chip>
        </div>

        <v-btn 
          color="error" 
          variant="outlined" 
          block 
          @click="logout"
          prepend-icon="mdi-logout"
        >
          Cerrar Sesión
        </v-btn>
      </UiParentCard>
    </v-col>

    <v-col cols="12" lg="8">
      <!-- Mensajes de éxito/error -->
      <v-alert
        v-if="successMessage"
        type="success"
        variant="tonal"
        closable
        class="mb-4"
        @click:close="successMessage = ''"
      >
        {{ successMessage }}
      </v-alert>

      <v-alert
        v-if="errorMessage"
        type="error"
        variant="tonal"
        closable
        class="mb-4"
        @click:close="errorMessage = ''"
      >
        {{ errorMessage }}
      </v-alert>

      <!-- Card de datos del perfil -->
      <UiParentCard class="mb-6">
        <template #title>
          <div class="d-flex justify-space-between align-center">
            <span style="color: #1CBC94">Datos del Perfil</span>
            <v-btn
              v-if="!isEditingProfile"
              color="#1CBC94"
              variant="outlined"
              size="small"
              @click="editProfile"
              prepend-icon="mdi-pencil"
            >
              Editar
            </v-btn>
          </div>
        </template>

        <v-form @submit.prevent="saveProfile">
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="profileData.username"
                label="Nombre de usuario"
                variant="outlined"
                density="compact"
                :readonly="!isEditingProfile"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="profileData.email"
                label="Email"
                variant="outlined"
                density="compact"
                :readonly="!isEditingProfile"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="profileData.firstName"
                label="Nombre"
                variant="outlined"
                density="compact"
                :readonly="!isEditingProfile"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="profileData.lastName"
                label="Apellidos"
                variant="outlined"
                density="compact"
                :readonly="!isEditingProfile"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="profileData.phone"
                label="Teléfono"
                variant="outlined"
                density="compact"
                :readonly="!isEditingProfile"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="profileData.location"
                label="Ubicación"
                variant="outlined"
                density="compact"
                :readonly="!isEditingProfile"
              />
            </v-col>
            <v-col cols="12">
              <v-textarea
                v-model="profileData.bio"
                label="Biografía"
                variant="outlined"
                density="compact"
                :readonly="!isEditingProfile"
                rows="3"
              />
            </v-col>
          </v-row>

          <div v-if="isEditingProfile" class="d-flex justify-end ga-4 mt-4">
            <v-btn
              color="grey"
              variant="outlined"
              @click="cancelEditProfile"
              :disabled="isLoading"
            >
              Cancelar
            </v-btn>
            <v-btn
              color="#1CBC94"
              variant="flat"
              type="submit"
              :loading="isLoading"
            >
              Guardar
            </v-btn>
          </div>
        </v-form>
      </UiParentCard>

      <!-- Card de cambio de contraseña -->
      <UiParentCard>
        <template #title>
          <div class="d-flex justify-space-between align-center">
            <span style="color: #1CBC94">Seguridad</span>
            <v-btn
              v-if="!isEditingPassword"
              color="#1CBC94"
              variant="outlined"
              size="small"
              @click="editPassword"
              prepend-icon="mdi-lock"
            >
              Cambiar Contraseña
            </v-btn>
          </div>
        </template>

        <div v-if="!isEditingPassword">
          <p class="text-body-2 text-grey">
            Tu contraseña fue actualizada por última vez hace 30 días.
          </p>
        </div>

        <v-form v-if="isEditingPassword" @submit.prevent="savePassword">
          <v-text-field
            v-model="passwordData.currentPassword"
            label="Contraseña actual"
            type="password"
            variant="outlined"
            density="compact"
            class="mb-4"
          />
          <v-text-field
            v-model="passwordData.newPassword"
            label="Nueva contraseña"
            type="password"
            variant="outlined"
            density="compact"
            class="mb-4"
          />
          <v-text-field
            v-model="passwordData.confirmPassword"
            label="Confirmar nueva contraseña"
            type="password"
            variant="outlined"
            density="compact"
            class="mb-4"
          />

          <div class="d-flex justify-end ga-4">
            <v-btn
              color="grey"
              variant="outlined"
              @click="cancelEditPassword"
              :disabled="isLoading"
            >
              Cancelar
            </v-btn>
            <v-btn
              color="#1CBC94"
              variant="flat"
              type="submit"
              :loading="isLoading"
            >
              Cambiar Contraseña
            </v-btn>
          </div>
        </v-form>
      </UiParentCard>
    </v-col>
  </v-row>
</template>