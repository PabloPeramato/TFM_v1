<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useAuthStore } from '../../stores/auth';
import { formatDeviceName } from '@/utils/helpers/format';
import MyDeviceCard from './components/MyDeviceCard.vue';

const authStore = useAuthStore();
const username = authStore.user?.username ?? '';
const unavailableDevices = ref<{ serial: string; os: string; user: string }[]>([]);

const myDevices = computed(() => {
    if (!Array.isArray(unavailableDevices.value)) return [];
    return unavailableDevices.value.filter(device => device.user === username);
});

onMounted(async () => {

    const token = localStorage.getItem('user');
    if (!token) return;
    const parsed = JSON.parse(token);
    const decoded = JSON.parse(atob(parsed.token.split('.')[1]));
    const username = decoded.data.userName;
    const useMock = import.meta.env.VITE_USE_MOCK === 'true';

    try {
        let res;
        if (useMock) {
            // --------------- 🔁 Modo mock  --------------
            res = {
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
            const flatDevices = res.data.operating_systems.flatMap(os =>
                os.serials.filter(s => s.trim() !== '').map(serial => ({
                    os: os.name,
                    serial,
                    user: username
                }))
            );
            unavailableDevices.value = flatDevices;
        }
        else {
            // --------------- LLAMADA A BACK  --------------
            res = await axios.get(`${import.meta.env.VITE_API_URL}/users/metadata?user=${username}`);

            const devices: { name: string; serials: string[] }[] = res.data.operating_systems || [];
            const flatDevices = devices.flatMap(os =>
                os.serials.filter(s => s.trim() !== '').map(serial => ({
                    os: os.name,
                    serial,
                    user: username
                }))
            );
            unavailableDevices.value = flatDevices;
        }
    } catch (error) {
        console.error('Error al obtener dispositivos del usuario:', error);
    }
});
</script>

<template>
    <v-row>
        <v-col cols="12">
            <h2 class="text-h3 font-weight-bold mb-4" style="color: #1db286">My devices</h2>
        </v-col>

        <v-col v-for="(device, index) in myDevices" :key="device.serial" cols="12" md="4">
            <MyDeviceCard :name="formatDeviceName(device.serial)" :serial="device.serial" :mounted="true" />
        </v-col>

        <v-col v-if="myDevices.length === 0" cols="12">
            <p class="text-center text-subtitle-1 text-grey-darken-1">
                You don't have devices assigned.
            </p>
        </v-col>
    </v-row>
</template>
