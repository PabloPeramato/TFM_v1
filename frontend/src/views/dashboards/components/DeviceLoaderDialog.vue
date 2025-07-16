<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  loading: Boolean
});
</script>

<template>
  <v-dialog v-model="props.loading" persistent width="300">
    <v-card class="pa-5 d-flex flex-column align-center justify-center">
      <v-progress-circular indeterminate color="primary" size="48" class="mb-4" />
      <span class="text-subtitle-1 font-weight-medium">Loading...</span>
    </v-card>
  </v-dialog>
</template>
