<script setup lang="ts">
import { onMounted, ref, shallowRef } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { useUserStore } from '@/stores/authSessions';
import axios from 'axios';
import { fillDeviceFormFields } from '@/utils/helpers/fillDeviceFormFields';

import BaseBreadcrumb from '@/components/shared/BaseBreadcrumb.vue';
import UiParentCard from '@/components/shared/UiParentCard.vue';

const route = useRoute();
const router = useRouter();
const serial = route.params.serial as string;
const authStore = useAuthStore();
const userStore = useUserStore();

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
    });
});

async function handleCreateImage() {
  router.back();
  try {
    
    console.log('Creating image with:', {
      user: formUser.value,
      os: formOs.value,
      serial: formSerial.value
    });
    const response = await userStore.newImage(formUser.value, formOs.value, formSerial.value);
    console.log('✅ Imagen creada correctamente:', response);
    // Mostrar notificación o redirigir
  } catch (err) {
    console.error(err);
    
    const errorString = String(err);
    
    if (errorString === 'Invalid argument' || errorString.includes('400')) {
      formError.value = 'Sistema operativo no válido';
    } else if (errorString === 'Invalid serial' || errorString.includes('401')) {
      formError.value = 'Serial no válido';
    } else if (errorString === 'Unmount' || errorString.includes('402')) {
      formError.value = 'Desmonte primero el dispositivo';
    } else if (errorString.includes('500') || errorString.includes('Internal Server Error')) {
      formError.value = 'Error interno del servidor. Inténtelo más tarde.';
    } else if (errorString.includes('network') || errorString.includes('Network')) {
      formError.value = 'Error de red. Verifica tu conexión';
    } else {
      formError.value = 'Error de autenticación. Verifica tus credenciales.';
    }
  }
}

async function handleMounted() {
  router.back();
  try {
    
    console.log('Mounting image with:', {
      user: formUser.value,
      os: formOs.value,
      serial: formSerial.value
    });
    const response = await userStore.mounted(formUser.value, formOs.value, formSerial.value);
    console.log('✅ Imagen montada correctamente:', response);
    // Mostrar notificación o redirigir
  } catch (err) {
    console.error(err);
    
    const errorString = String(err);
    
    if (errorString === 'Invalid argument' || errorString.includes('400')) {
      formError.value = 'Sistema operativo no válido';
    } else if (errorString === 'Invalid serial' || errorString.includes('401')) {
      formError.value = 'Serial no válido';
    } else if (errorString === 'Unmount' || errorString.includes('402')) {
      formError.value = 'Desmonte primero el dispositivo';
    } else if (errorString.includes('500') || errorString.includes('Internal Server Error')) {
      formError.value = 'Error interno del servidor. Inténtelo más tarde.';
    } else if (errorString.includes('network') || errorString.includes('Network')) {
      formError.value = 'Error de red. Verifica tu conexión';
    } else {
      formError.value = 'Error de autenticación. Verifica tus credenciales.';
    }
  }
}

async function handleDisMounted() {
  router.back();
  try {
    
    console.log('Dismounting image with:', {
      user: formUser.value,
      os: formOs.value,
      serial: formSerial.value
    });
    const response = await userStore.dismounted(formUser.value, formOs.value, formSerial.value);
    console.log('✅ Imagen desmontada correctamente:', response);
    // Mostrar notificación o redirigir
  } catch (err) {
    console.error(err);
    
    const errorString = String(err);
    
    if (errorString === 'Invalid argument' || errorString.includes('400')) {
      formError.value = 'Sistema operativo no válido';
    } else if (errorString === 'Invalid serial' || errorString.includes('401')) {
      formError.value = 'Serial no válido';
    } else if (errorString === 'PowerOFF' || errorString.includes('403')) {
      formError.value = 'Apague primero el dispositivo';
    } else if (errorString.includes('500') || errorString.includes('Internal Server Error')) {
      formError.value = 'Error interno del servidor. Inténtelo más tarde.';
    } else if (errorString.includes('network') || errorString.includes('Network')) {
      formError.value = 'Error de red. Verifica tu conexión';
    } else {
      formError.value = 'Error de autenticación. Verifica tus credenciales.';
    }
  }
}

async function handleDelete() {
  router.back();
  try {
    
    console.log('Deleting image with:', {
      user: formUser.value,
      os: formOs.value,
      serial: formSerial.value
    });
    const response = await userStore.delete(formUser.value, formOs.value, formSerial.value);
    console.log('✅ Imagen eliminada correctamente:', response);
    // Mostrar notificación o redirigir
  } catch (err) {
    console.error(err);
    
    const errorString = String(err);
    
    if (errorString === 'Invalid argument' || errorString.includes('400')) {
      formError.value = 'Sistema operativo no válido';
    } else if (errorString === 'Invalid serial' || errorString.includes('401')) {
      formError.value = 'Serial no válido';
    } else if (errorString === 'Unmount' || errorString.includes('402')) {
      formError.value = 'Desmonte primero el dispositivo';
    } else if (errorString === 'Not found' || errorString.includes('405')) {
      formError.value = 'Sistema operativo no registrado en la sesión';
    } else if (errorString.includes('500') || errorString.includes('Internal Server Error')) {
      formError.value = 'Error interno del servidor. Inténtelo más tarde.';
    } else if (errorString.includes('network') || errorString.includes('Network')) {
      formError.value = 'Error de red. Verifica tu conexión';
    } else {
      formError.value = 'Error de autenticación. Verifica tus credenciales.';
    }
  }
}
</script>

<template>
  <BaseBreadcrumb :title="page.title" :breadcrumbs="breadcrumbs" />

  <v-row>
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
          <v-btn size="small" variant="flat" color="grey" @click="handleMounted">Mounted</v-btn>
          <v-btn size="small" variant="flat" color="grey" @click="handleDisMounted">Dismounted</v-btn>
          <v-btn size="small" variant="flat" color="#1CBC94" @click="handleCreateImage">Create New Image</v-btn>
          <v-btn size="small" variant="flat" color="error" @clicl="handleDelete">Delete</v-btn>
        </div>

        <div class="mb-2 font-weight-medium">New image</div>
        <div class="text-caption mb-4">Complete the form to create a new image of the device</div>

        <v-text-field v-model="formUser" label="User" variant="outlined" density="compact" />
        <v-text-field v-model="formOs" label="Operating system and Raspberry Pi model" variant="outlined"
          density="compact" />
        <v-text-field v-model="formSerial" label="Serial number" variant="outlined" density="compact" />

        <div class="d-flex justify-end mt-4 ga-4">
          <!--v-btn color="#1CBC94" variant="flat" size="small">Create</v-btn-->
          <v-btn color="grey" variant="flat" size="small" @click="handleCancel">Cancel</v-btn>
        </div>
      </UiParentCard>
    </v-col>
  </v-row>
</template>
