<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useAuthStore } from '../../../stores/auth';
import { formatDeviceName } from '@/utils/helpers/format';
import MyDeviceCard from '../components/MyDeviceCard.vue';
import DeviceLoaderDialog from '@/views/dashboards/components/DeviceLoaderDialog.vue';

const authStore = useAuthStore();
const username = authStore.user?.username ?? '';
const unavailableDevices = ref<{ serial: string; os: string; user: string }[]>([]);
const loading = ref(true);
const powerStatus = ref<{ serial: string; os: string; power_status: string; ip: string }[]>([]);

const myDevices = computed(() => {
  if (!Array.isArray(unavailableDevices.value)) return [];
  return unavailableDevices.value.filter((device) => device.user === username);
});

onMounted(async () => {
  const token = localStorage.getItem('user');
  if (!token) {
    loading.value = false;
    return;
  }

  const parsed = JSON.parse(token);
  const decoded = JSON.parse(atob(parsed.token.split('.')[1]));
  const username = decoded.data.userName;
  const useMock = import.meta.env.VITE_USE_MOCK === 'true';

  try {
    let flatDevices = [];

    if (useMock) {
      const mockResponse = {
        data: {
          user: username,
          operating_systems: [
            {
              name: 'PI-3B-RASPBIAN',
              serials: ['8ba14c83']
            },
            {
              name: 'PI-3B-DIETPI',
              serials: ['81b715b7']
            }
          ]
        }
      };

      flatDevices = mockResponse.data.operating_systems.flatMap((os) =>
        os.serials
          .filter((s) => s.trim() !== '')
          .map((serial) => ({
            os: os.name,
            serial,
            user: username
          }))
      );
    } else {
      const res = await axios.get(`${import.meta.env.VITE_API_URL}/users/metadata`, {
        params: { user: username }
      });
      console.log('Respuesta del endpoint /users/metadata:', res.data);

      const devices = res.data.operating_systems || [];
      flatDevices = devices.flatMap((os: { name: string; serials: string[] }) =>
        os.serials
          .filter((s) => s.trim() !== '')
          .map((serial) => ({
            os: os.name,
            serial,
            user: username
          }))
      );
    }

    if (flatDevices.length > 0) {
      try {
        const statusRes = await axios.get(`${import.meta.env.VITE_API_URL}/power/status`, {
          params: { user: username }
        });

        console.log('Respuesta del endpoint /power/status:', statusRes.data);

        powerStatus.value = statusRes.data.power_status;

        const powerSerials = new Set(powerStatus.value.map((p) => p.serial));
        unavailableDevices.value = flatDevices.filter((device) => powerSerials.has(device.serial));
      } catch (err) {
        console.warn('No se pudo obtener el estado de encendido:', err?.response?.data?.detail ?? err.message);
        powerStatus.value = [];
        unavailableDevices.value = [];
      }
    }
  } catch (error) {
    console.error(' Error general al cargar dispositivos del usuario:', error);
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <DeviceLoaderDialog :loading="loading" />
  <v-row v-if="!loading">
    <v-col cols="12">
      <h2 class="text-h3 font-weight-bold mb-4" style="color: #1db286">My devices</h2>
    </v-col>

    <v-col v-for="device in myDevices" :key="device.serial" cols="12" md="4">
      <MyDeviceCard
        :name="formatDeviceName(device.serial)"
        :serial="device.serial"
        :os="device.os"
        :mounted="true"
        :power-info="powerStatus.find((p) => p.serial === device.serial)"
        :username="username"
      />
    </v-col>

    <v-col v-if="myDevices.length === 0" cols="12">
      <p class="text-center text-subtitle-1 text-grey-darken-1">You don't have devices assigned.</p>
    </v-col>
  </v-row>
</template>
