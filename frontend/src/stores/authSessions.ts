import { defineStore } from 'pinia';
import { router } from '@/router';
import { fetchWrapper } from '@/utils/helpers/fetch-wrapper';
import { jwtDecode } from 'jwt-decode';

const apiUrl = import.meta.env.VITE_API_URL || '';
const baseUrl = `${apiUrl}/sessions`;

export const useUserStore = defineStore({
  id: 'usersessions',
  state: () => ({
    // initialize state from local storage to enable user to stay logged in
    /* eslint-disable-next-line @typescript-eslint/ban-ts-comment */
    // @ts-ignore
    user: JSON.parse(localStorage.getItem('user')),
    returnUrl: null
  }),

  actions: {
    async newImage(user: string, os: string, serial: string) {
      const url = `${baseUrl}/newImage`;
      const params = new URLSearchParams({
        user: user,
        os: os,
        serial: serial
      }).toString();
      console.log('🔄 Enviando nueva imagen:', params);
      const response = await fetchWrapper.post(`${url}?${params}`);
      return response;
    },
    async mounted(user: string, os: string, serial: string) {
      const url = `${baseUrl}/mount`;
      const params = new URLSearchParams({
        user: user,
        os: os,
        serial: serial
      }).toString();
      console.log('🔄 Montando imagen:', params);
      const response = await fetchWrapper.post(`${url}?${params}`);
      return response;
    },
    async dismounted(user: string, os: string, serial: string) {
      const url = `${baseUrl}/dismount`;
      const params = new URLSearchParams({
        user: user,
        os: os,
        serial: serial
      }).toString();
      console.log('🔄 Desmontando imagen:', params);
      const response = await fetchWrapper.post(`${url}?${params}`);
      return response;
    },
    async delete(user: string, os: string, serial: string) {
      const url = `${baseUrl}/delete`;
      const params = new URLSearchParams({
        user: user,
        os: os,
        serial: serial
      }).toString();
      console.log('🔄 Eliminando imagen:', params);
      const response = await fetchWrapper.post(`${url}?${params}`);
      return response;
    },
  }
});
