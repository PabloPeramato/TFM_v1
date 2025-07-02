<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const softwareAvailability = ref(null);

onMounted(() => {
  axios
    .get(`${import.meta.env.VITE_API_URL}/availability/software`)
    .then((res) => {
      softwareAvailability.value = res.data;
    })
    .catch((err) => console.error("API error:", err));
});
</script>

<template>
  <main>
    <h1>Disponibilidad de software</h1>

    <div v-if="softwareAvailability">
      <ul>
        <li v-for="(item, index) in softwareAvailability" :key="index">
          {{ item }}
        </li>
      </ul>
    </div>

    <p v-else>Cargando disponibilidad de software...</p>
  </main>
</template>
