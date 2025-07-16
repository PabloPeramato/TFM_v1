<script setup lang="ts">
import { onMounted, ref, shallowRef } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { useUserStore } from '@/stores/authSessions';
import axios from 'axios';
import { fillDeviceFormFields } from '@/utils/helpers/fillDeviceFormFields';

import BaseBreadcrumb from '@/components/shared/BaseBreadcrumb.vue';
import UiParentCard from '@/components/shared/UiParentCard.vue';
import DeviceLoaderDialog from '@/views/dashboards/components/DeviceLoaderDialog.vue'; // ajusta la ruta si es distinta

const route = useRoute();
const router = useRouter();
const serial = route.params.serial as string;
const authStore = useAuthStore();
const userStore = useUserStore();
const loading = ref(true);

const page = ref({ title: 'Device details' });
const breadcrumbs = shallowRef([
  { title: 'Devices', disabled: false, href: '/devices' },
  { title: 'Details', disabled: true, href: '#' }
]);

type Device = { serial: string; os: string; user: string };

const device = ref<null | Device>(null);
const deviceStatus = ref<'Available' | 'Not Available'>('Not Available');
const piIndex = ref<number | null>(null);

const formUser = ref(authStore.user?.username || '');
const formOs = ref('');
const formSerial = ref('');
const formError = ref('');
const mountingLoading = ref(false);
const dismountingLoading = ref(false);
const newImageLoading = ref(false);
const deleteLoading = ref(false);

function handleCancel() {
  router.back();
}

onMounted(() => {
  axios
    .get(`${import.meta.env.VITE_API_URL}/availability/hardware`)
    .then((res) => {
      const unavailable = res.data.unavailable as Device[];
      const available = res.data.available as string[];

      const unavailableIndex = unavailable.findIndex((d) => d.serial === serial);
      if (unavailableIndex !== -1) {
        deviceStatus.value = 'Not Available';
        device.value = unavailable[unavailableIndex];
        piIndex.value = unavailableIndex + 1;
      } else {
        const availableIndex = available.findIndex((s) => s === serial);
        if (availableIndex !== -1) {
          deviceStatus.value = 'Available';
          device.value = { serial, os: '-', user: '-' };
          piIndex.value = availableIndex + 1;
        }
      }

      if (device.value) {
        fillDeviceFormFields(device.value, formUser, formOs, formSerial, authStore.user?.username || '');
      }
    })
    .catch((err) => {
      console.error('Error fetching device:', err);
    })
    .finally(() => {
      loading.value = false;
    });
});

async function handleCreateImage() {
  formError.value = '';
  newImageLoading.value = true;
  try {
    console.log('Creating image with:', {
      user: formUser.value,
      os: formOs.value,
      serial: formSerial.value
    });
    const response = await userStore.newImage(formUser.value, formOs.value, formSerial.value);
    console.log('✅ Imagen creada correctamente:', response);
    // Mostrar notificación o redirigir
  } catch (err: any) {
    const statusCode = err.response?.status;
    const backendDetail = err.response?.data?.detail || '';

    if (statusCode === 400) {
      console.error('Invalid argument error:', backendDetail);
      formError.value = 'Sistema operativo no válido';
    } else if (statusCode === 401) {
      console.error('Unauthorized error:', backendDetail);
      formError.value = 'Serial no válido';
    } else if (statusCode === 402) {
      console.error('Payment Required error:', backendDetail);
      formError.value = 'Desmonte primero el dispositivo';
    } else if (statusCode === 500) {
      console.error('Internal Server Error:', backendDetail);
      formError.value = 'Error interno del servidor. Inténtelo más tarde.';
    } else if (err.message.toLowerCase().includes('network')) {
      formError.value = 'Error de red. Verifica tu conexión';
    } else {
      console.error('Other error:', backendDetail);
      formError.value = 'Error de autenticación. Verifica tus credenciales.';
    }
  } finally {
    newImageLoading.value = false;
  }
}

async function handleMounted() {
  formError.value = '';
  mountingLoading.value = true;
  try {
    console.log('Mounting image with:', {
      user: formUser.value,
      os: formOs.value,
      serial: formSerial.value
    });
    const response = await userStore.mounted(formUser.value, formOs.value, formSerial.value);
    console.log('✅ Imagen montada correctamente:', response);
    // Mostrar notificación o redirigir
  } catch (err: any) {
    const statusCode = err.response?.status;
    const backendDetail = err.response?.data?.detail || '';

    if (statusCode === 400) {
      console.error('Invalid argument error:', backendDetail);
      formError.value = 'Sistema operativo no válido';
    } else if (statusCode === 401) {
      console.error('Unauthorized error:', backendDetail);
      formError.value = 'Serial no válido';
    } else if (statusCode === 402) {
      console.error('Payment Required error:', backendDetail);
      formError.value = 'Desmonte primero el dispositivo';
    } else if (statusCode === 407) {
      console.error('Proxy Authentication Required error:', backendDetail);
      formError.value = 'No hay sesiones para el usuario.';
    } else if (statusCode === 408) {
      console.error('Request Timeout error:', backendDetail);
      formError.value = 'No hay sesiones para este SO';
    } else if (statusCode === 409) {
      console.error('Conflict error:', backendDetail);
      formError.value = 'No hay sesión para este dispositivo';
    } else if (statusCode === 500) {
      console.error('Internal Server Error:', backendDetail);
      formError.value = 'Error interno del servidor. Inténtelo más tarde.';
    } else if (err.message.toLowerCase().includes('network')) {
      formError.value = 'Error de red. Verifica tu conexión';
    } else {
      console.error('Other error:', backendDetail);
      formError.value = 'Error de autenticación. Verifica tus credenciales.';
    }
  } finally {
    mountingLoading.value = false;
  }
}

async function handleDisMounted() {
  formError.value = '';
  dismountingLoading.value = true;
  try {
    console.log('Dismounting image with:', {
      user: formUser.value,
      os: formOs.value,
      serial: formSerial.value
    });
    const response = await userStore.dismounted(formUser.value, formOs.value, formSerial.value);
    console.log('✅ Imagen desmontada correctamente:', response);
    // Mostrar notificación o redirigir
  } catch (err: any) {
    const statusCode = err.response?.status;
    const backendDetail = err.response?.data?.detail || '';

    if (statusCode === 400) {
      console.error('Invalid argument error:', backendDetail);
      formError.value = 'Sistema operativo no válido';
    } else if (statusCode === 401) {
      console.error('Unauthorized error:', backendDetail);
      formError.value = 'Serial no válido';
    } else if (statusCode === 403) {
      console.error('Forbidden error:', backendDetail);
      formError.value = 'Apague primero el dispositivo';
    } else if (statusCode === 405) {
      console.error('Method Not Allowed error:', backendDetail);
      formError.value = 'Raspberry Pi no montada';
    } else if (statusCode === 407) {
      console.error('Proxy Authentication Required error:', backendDetail);
      formError.value = 'No hay sesiones para el usuario.';
    } else if (statusCode === 408) {
      console.error('Request Timeout error:', backendDetail);
      formError.value = 'No hay sesiones para este SO';
    } else if (statusCode === 409) {
      console.error('Conflict error:', backendDetail);
      formError.value = 'No hay sesión para este dispositivo';
    } else if (statusCode === 500) {
      console.error('Internal Server Error:', backendDetail);
      formError.value = 'Error interno del servidor. Inténtelo más tarde.';
    } else if (err.message.toLowerCase().includes('network')) {
      formError.value = 'Error de red. Verifica tu conexión';
    } else {
      console.error('Other error:', backendDetail);
      formError.value = 'Error de autenticación. Verifica tus credenciales.';
    }
  } finally {
    dismountingLoading.value = false;
  }
}

async function handleDelete() {
  formError.value = '';
  deleteLoading.value = true;
  try {
    console.log('Deleting image with:', {
      user: formUser.value,
      os: formOs.value,
      serial: formSerial.value
    });
    const response = await userStore.delete(formUser.value, formOs.value, formSerial.value);
    console.log('✅ Imagen eliminada correctamente:', response);
    // Mostrar notificación o redirigir
  } catch (err: any) {
    const statusCode = err.response?.status;
    const backendDetail = err.response?.data?.detail || '';

    if (statusCode === 400) {
      console.error('Invalid argument error:', backendDetail);
      formError.value = 'Sistema operativo no válido';
    } else if (statusCode === 401) {
      console.error('Unauthorized error:', backendDetail);
      formError.value = 'Serial no válido';
    } else if (statusCode === 402) {
      console.error('Unmount first error:', backendDetail);
      formError.value = 'Desmonte primero el dispositivo';
    } else if (statusCode === 406) {
      console.error('Not found error:', backendDetail);
      formError.value = 'Sistema operativo no registrado en la sesión';
    } else if (statusCode === 407) {
      console.error('No session for user:', backendDetail);
      formError.value = 'No hay sesiones para el usuario.';
    } else if (statusCode === 408) {
      console.error('No session for OS:', backendDetail);
      formError.value = 'No hay sesiones para este SO';
    } else if (statusCode === 409) {
      console.error('No session for OS and serial:', backendDetail);
      formError.value = 'No hay sesión para este dispositivo';
    } else if (statusCode === 500) {
      console.error('Internal Server Error:', backendDetail);
      formError.value = 'Error interno del servidor. Inténtelo más tarde.';
    } else if (err.message.toLowerCase().includes('network')) {
      formError.value = 'Error de red. Verifica tu conexión';
    } else {
      console.error('Other error:', backendDetail);
      formError.value = 'Error de autenticación. Verifica tus credenciales.';
    }
  } finally {
    deleteLoading.value = false;
  }
}
</script>

<template>
  <DeviceLoaderDialog :loading="loading" />

  <BaseBreadcrumb v-if="!loading" :title="page.title" :breadcrumbs="breadcrumbs" />

  <v-row v-if="!loading">
    <v-col cols="12" md="12">
      <UiParentCard v-if="device">
        <template #title>
          <span style="color: #1db286">Device details</span>
        </template>

        <v-card class="pa-6 mb-6 rounded-xl bg-grey-lighten-4" elevation="1">
          <div class="d-flex justify-space-between align-center mb-2">
            <span class="text-subtitle-2">{{ deviceStatus }}</span>
            <v-icon :color="deviceStatus === 'Available' ? '#1CBC94' : '#D95262'">
              {{ deviceStatus === 'Available' ? 'mdi-check-circle' : 'mdi-close-circle' }}
            </v-icon>
          </div>

          <h2 class="text-h5 font-weight-bold mb-1">Raspberry Pi {{ piIndex !== null ? `(${piIndex})` : '' }}</h2>

          <div class="text-caption">Serial: {{ device?.serial || serial }}</div>
        </v-card>

        <div class="mb-2 font-weight-medium">Device options</div>
        <div class="d-flex ga-4 mb-6">
          <v-btn size="small" variant="flat" color="grey" @click="handleMounted" :disabled="mountingLoading">
            {{ mountingLoading ? 'Mounting...' : 'Mount' }}
          </v-btn>
          <v-btn size="small" variant="flat" color="grey" @click="handleDisMounted" :disabled="dismountingLoading">
            {{ dismountingLoading ? 'Dismounting...' : 'Dismount' }}
          </v-btn>
          <v-btn size="small" variant="flat" color="#1CBC94" @click="handleCreateImage" :disabled="newImageLoading">
            {{ newImageLoading ? 'Creating New Image...' : 'Create New Image' }}
          </v-btn>
          <v-btn size="small" variant="flat" color="error" @click="handleDelete" :disabled="deleteLoading">
            {{ deleteLoading ? 'Deleting...' : 'Delete' }}
          </v-btn>
        </div>

        <!--div class="mb-2 font-weight-medium">New image</div-->
        <div class="text-caption mb-4">Complete the form to manage the device</div>
        <div v-if="formError" class="error-message">
          {{ formError }}
        </div>

        <v-text-field v-model="formUser" label="User" variant="outlined" density="compact" readonly />
        <v-select
          v-model="formOs"
          :items="['dietpi', 'raspbian']"
          label="Operating system and Raspberry Pi model"
          placeholder="Selecciona el sistema operativo"
          variant="outlined"
          density="compact"
          clearable
          persistent-placeholder
        />
        <v-text-field v-model="formSerial" label="Serial number" variant="outlined" density="compact" readonly />

        <div class="d-flex justify-end mt-4 ga-4">
          <!--v-btn color="#1CBC94" variant="flat" size="small">Create</v-btn-->
          <v-btn color="grey" variant="flat" size="small" @click="handleCancel">Cancel</v-btn>
        </div>
      </UiParentCard>
    </v-col>
  </v-row>
</template>

<style scoped>
.error-message {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
  padding: 8px 12px;
  margin: 8px 0;
  font-size: 14px;
  width: 100%;
  text-align: center;
}
</style>
