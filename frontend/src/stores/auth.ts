import { defineStore } from 'pinia';
import { router } from '@/router';
import { fetchWrapper } from '@/utils/helpers/fetch-wrapper';
import { jwtDecode } from 'jwt-decode';

const apiUrl = import.meta.env.VITE_API_URL || '';
const baseUrl = `${apiUrl}/account`;

export const useAuthStore = defineStore({
  id: 'auth',
  state: () => ({
    // initialize state from local storage to enable user to stay logged in
    /* eslint-disable-next-line @typescript-eslint/ban-ts-comment */
    // @ts-ignore
    user: JSON.parse(localStorage.getItem('user')),
    returnUrl: null
  }),

  actions: {
    async login(loginField: string, password: string) {
      const url = `${baseUrl}/login`;
      const params = new URLSearchParams({
        login_field: loginField,
        password
      }).toString();

      const response = await fetchWrapper.post(`${url}?${params}`);

      if (!response.token || typeof response.token !== 'string') {
        console.error('❌ Token inválido:', response.token);
        throw new Error('Token inválido');
      }

      // ⬇️ Decodificamos el token con seguridad
      let username = '';
      try {
        const decoded: any = jwtDecode(response.token);
        username = decoded?.data?.userName ?? '';
        console.log('✅ Usuario decodificado:', username);
      } catch (err) {
        console.error('❌ Error decodificando el token:', err);
        throw new Error('Token mal formado');
      }

      this.user = {
        token: response.token,
        username
      };

      localStorage.setItem('user', JSON.stringify(this.user));
      router.push(this.returnUrl || '/dashboard/default');
    },

    async register(mail: string, username: string, password: string, confirmPassword: string) {
      const url = `${baseUrl}/register`;
      const params = new URLSearchParams({
        mail,
        username,
        password,
        confirm_password: confirmPassword
      }).toString();
      await fetchWrapper.post(`${url}?${params}`);
    },
    logout() {
      this.user = null;
      localStorage.removeItem('user');
      router.push('/auth/login');
    }
  }
});
