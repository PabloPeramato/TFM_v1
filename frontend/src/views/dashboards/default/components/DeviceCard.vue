<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();

const props = defineProps<{
  name: string;
  serial: string;
  status: 'Available' | 'Not Available';
  mounted: boolean;
}>();

const goToDetails = () => {
  router.push(`/devices/${props.serial}`);
};
</script>

<template>
  <v-card elevation="2" class="pa-4 rounded-xl d-flex flex-column justify-space-between h-100">
    <div>
      <div class="d-flex justify-space-between align-center mb-2">
        <span class="text-subtitle-2">{{ props.status }}</span>
        <v-icon :color="props.status === 'Available' ? '#1CBC94' : props.mounted ? '#F3A600' : '#D95262'">
          {{ props.status === 'Available' ? 'mdi-check-circle' : props.mounted ? 'mdi-power' : 'mdi-close-circle' }}
        </v-icon>
      </div>

      <h2 class="text-h2 font-weight-bold mb-1">{{ props.name }}</h2>

      <div class="text-caption mb-3">Serial {{ props.serial }}</div>
    </div>

    <v-btn
      :color="props.status === 'Available' ? '#1CBC94' : ''"
      variant="flat"
      class="align-self-start mt-4"
      @click="goToDetails"
      :disabled="props.mounted"
    >
      View details
    </v-btn>
  </v-card>
</template>
