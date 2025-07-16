<script setup lang="ts">
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import { computed } from 'vue';
import axios from 'axios';

const formattedOs = computed(() => {
  if (props.os === 'PI-3B-RASPBIAN-BULLSEYE') return 'Raspbian';
  if (props.os === 'PI-3B-DIETPI-BOOKWORM') return 'Dietpi';
  return 'Unknown OS';
});

const router = useRouter();

const props = defineProps({
  name: String,
  serial: String,
  os: String,
  status: String,
  mounted: Boolean,
  showStatus: {
    type: Boolean,
    default: true
  },
  powerInfo: {
    type: Object as () => { serial: string; os: string; power_status: string; ip: string } | undefined,
    required: false
  },
  username: {
    type: String,
    required: true
  }
});
console.log('[MyDeviceCard] Props recibidas:', {
  name: props.name,
  serial: props.serial,
  os: props.os,
  powerInfo: props.powerInfo
});

const goToDetails = () => {
  if (props.serial?.trim()) {
    router.push({
      name: 'MyDeviceDetails',
      params: { serial: props.serial },
      query: { os: props.os }
    });
  }
};

const power = ref(props.powerInfo?.power_status === 'on');

watch(power, async (newVal, oldVal) => {
  if (newVal === oldVal || !props.powerInfo) return;

  const endpoint = newVal ? '/power/on' : '/power/off';
  try {
    await axios.post(`${import.meta.env.VITE_API_URL}${endpoint}`, null, {
      params: { user: props.username }
    });
    console.log(`${props.serial} turned ${newVal ? 'on' : 'off'}`);
  } catch (error) {
    console.error(`Failed to turn ${newVal ? 'on' : 'off'} ${props.serial}`, error);
    power.value = oldVal;
  }
});
</script>
<template>
  <v-card elevation="2" class="pa-4 rounded-xl d-flex flex-column justify-space-between h-100 position-relative">
    <div>
      <h2 class="text-h2 font-weight-bold mb-2">{{ props.name }}</h2>
      <h3 v-if="props.os !== 'None'" class="text-h6 mb-4" style="color: #1db286">
        {{ formattedOs || 'Unknown OS' }}
      </h3>

      <div class="text-caption mb-3">Serial {{ props.serial }}</div>
    </div>
    <div
      v-if="props.powerInfo && props.powerInfo.os !== 'None' && props.powerInfo.power_status"
      style="position: absolute; top: 16px; right: 16px"
    >
      <v-switch v-model="power" color="success" density="compact" hide-details class="ma-0 pa-0" style="transform: scale(0.6)" />
    </div>

    <v-btn color="#1CBC94" variant="flat" class="align-self-start mt-auto" @click="goToDetails"> View Details </v-btn>
  </v-card>
</template>
