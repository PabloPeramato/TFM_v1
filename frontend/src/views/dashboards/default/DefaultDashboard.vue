<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import DeviceCard from './components/DeviceCard.vue';

const availableDevices = ref<string[]>([]);
const unavailableDevices = ref<{ serial: string; os: string; user: string }[]>([]);

onMounted(() => {
  axios
    .get(`${import.meta.env.VITE_API_URL}/availability/hardware`)
    .then((res) => {
      availableDevices.value = res.data.available;
      unavailableDevices.value = res.data.unavailable;
    })
    .catch((err) => console.error('API error:', err));
});
</script>

<template>
  <v-row>
    <v-col cols="12">
      <h2 class="text-h3 font-weight-bold mb-4" style="color: #1db286">Dismounted devices</h2>
    </v-col>
    <v-col v-for="(serial, index) in availableDevices" :key="'available-' + serial" cols="12" md="4">
      <DeviceCard :name="`RaspBerry Pi ${index + 1}`" :serial="serial" status="Available" :mounted="false" />
    </v-col>

    <v-col cols="12">
      <h2 class="text-h3 font-weight-bold mb-4" style="color: #1db286">Mounted devices</h2>
    </v-col>
    <v-col v-for="(device, index) in unavailableDevices" :key="'unavailable-' + device.serial" cols="12" md="4">
      <DeviceCard
        :name="`RaspBerry Pi ${availableDevices.length + index + 1}`"
        :serial="device.serial"
        status="Not Available"
        :mounted="true"
      />
    </v-col>
  </v-row>
</template>
