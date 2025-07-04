import { defineStore } from 'pinia';
import { router } from '@/router';
import { fetchWrapper } from '@/utils/helpers/fetch-wrapper';

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

      // update pinia state with received token
      this.user = { token: response.access_token };
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
