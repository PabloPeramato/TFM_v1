<template>
  <v-card elevation="2" class="pa-4 rounded-xl d-flex flex-column justify-space-between h-100 position-relative">
    <div>
      <h2 class="text-h2 font-weight-bold mb-2">{{ props.name }}</h2>
      <div class="text-caption mb-3">Serial {{ props.serial }}</div>
    </div>
    <div style="position: absolute; top: 16px; right: 16px;">
      <v-switch v-model="power" color="success" density="compact" hide-details class="ma-0 pa-0"
        style="transform: scale(0.6);" />
    </div>

    <v-btn color="#1CBC94" variant="flat" class="align-self-start mt-auto" @click="goToDetails">
      View Details
    </v-btn>
  </v-card>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const props = defineProps({
  name: String,
  serial: String,
  status: {
    type: String,
    required: false
  },
  mounted: Boolean,
  showStatus: {
    type: Boolean,
    default: true
  }
});

const goToDetails = () => {
  if (props.serial?.trim()) {
    router.push(`/main/my-devices/${props.serial}`);
  }
};

const power = ref(props.mounted);

watch(power, (newVal, oldVal) => {
  if (newVal !== oldVal) {
    console.log(`🔌 ${props.serial}:`, newVal ? 'Encendido' : 'Apagado');
  }
});
</script>
