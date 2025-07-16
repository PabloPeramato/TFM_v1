<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import DeviceCard from '../components/DeviceCard.vue';
import SearchBarPanel from '@/layouts/full/vertical-header/SearchBarPanel.vue'; // Ajusta ruta si es necesario
import { formatDeviceName } from '@/utils/helpers/format';
import DeviceLoaderDialog from '../components/DeviceLoaderDialog.vue';

const availableDevices = ref<string[]>([]);
const unavailableDevices = ref<{ serial: string; os: string; user: string }[]>([]);
const searchText = ref('');
const loading = ref(true);

onMounted(() => {
  axios
    .get(`${import.meta.env.VITE_API_URL}/availability/hardware`)
    .then((res) => {
      availableDevices.value = res.data.available;
      unavailableDevices.value = res.data.unavailable;
    })
    .catch((err) => console.error('API error:', err))
    .finally(() => {
      loading.value = false;
    });
});

const filteredAvailableDevices = computed(() => {
  const query = searchText.value?.toLowerCase() ?? '';
  return availableDevices.value.filter((serial) => {
    const name = formatDeviceName(serial)?.toLowerCase() ?? '';
    return name.includes(query) || serial?.toLowerCase().includes(query);
  });
});

const filteredUnavailableDevices = computed(() => {
  const query = searchText.value?.toLowerCase() ?? '';
  return unavailableDevices.value.filter((device) => {
    const name = formatDeviceName(device.serial)?.toLowerCase() ?? '';
    return name.includes(query) || device.serial?.toLowerCase().includes(query);
  });
});
</script>

<template>
  <DeviceLoaderDialog :loading="loading" />
  <v-row v-if="!loading">
    <v-col cols="12">
      <SearchBarPanel v-model="searchText" />
    </v-col>

    <v-col cols="12">
      <h2 class="text-h3 font-weight-bold mb-4" style="color: #1db286">Dismounted devices</h2>
    </v-col>
    <v-col v-for="serial in filteredAvailableDevices" :key="'available-' + serial" cols="12" md="4">
      <DeviceCard :name="formatDeviceName(serial)" :serial="serial" status="Available" :mounted="false" />
    </v-col>

    <v-col cols="12">
      <h2 class="text-h3 font-weight-bold mb-4" style="color: #1db286">Mounted devices</h2>
    </v-col>
    <v-col v-for="device in filteredUnavailableDevices" :key="'unavailable-' + device.serial" cols="12" md="4">
      <DeviceCard :name="formatDeviceName(device.serial)" :serial="device.serial" status="Not Available" :mounted="true" />
    </v-col>
  </v-row>
</template>
