import { defineStore } from 'pinia';
import { router } from '@/router';
import { fetchWrapper } from '@/utils/helpers/fetch-wrapper';

const baseUrl = `${import.meta.env.VITE_API_URL}/account`;

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
      const url = `${baseUrl}/login?login_field=${encodeURIComponent(loginField)}&password=${encodeURIComponent(password)}`;
      const response = await fetchWrapper.post(url);

      // update pinia state with received token
      this.user = { token: response.access_token };
      localStorage.setItem('user', JSON.stringify(this.user));
      router.push(this.returnUrl || '/dashboard/default');
    },

    async register(mail: string, username: string, password: string, confirmPassword: string) {
      const url = `${baseUrl}/register?mail=${encodeURIComponent(mail)}&username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}&confirm_password=${encodeURIComponent(confirmPassword)}`;
      await fetchWrapper.post(url);
    },
    logout() {
      this.user = null;
      localStorage.removeItem('user');
      router.push('/auth/login');
    }
  }
});
