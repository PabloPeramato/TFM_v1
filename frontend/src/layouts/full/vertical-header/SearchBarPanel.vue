<script setup>
import { SearchIcon, XIcon } from 'vue-tabler-icons';
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  modelValue: String,
  closesearch: Function
});

const emit = defineEmits(['update:modelValue']);

function clearSearch() {
  emit('update:modelValue', '');
  if (props.closesearch) props.closesearch();
}
</script>

<template>
  <v-text-field
    :model-value="props.modelValue"
    @update:modelValue="emit('update:modelValue', $event)"
    persistent-placeholder
    placeholder="Search Raspberry..."
    color="primary"
    variant="outlined"
    hide-details
    clearable
    class="mb-4"
  >
    <template #prepend-inner>
      <SearchIcon stroke-width="1.5" size="17" class="text-lightText SearchIcon" />
    </template>
    <template #append-inner>
      <v-btn
        color="lighterror"
        icon
        rounded="sm"
        variant="flat"
        size="small"
        class="text-error ml-3 d-block d-lg-none"
        @click="clearSearch"
      >
        <XIcon stroke-width="1.5" size="20" />
      </v-btn>
    </template>
  </v-text-field>
</template>
