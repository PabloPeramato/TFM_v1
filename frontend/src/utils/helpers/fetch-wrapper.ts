import { useAuthStore } from '@/stores/auth';

export const fetchWrapper = {
  get: request('GET'),
  post: request('POST'),
  put: request('PUT'),
  delete: request('DELETE')
};

interface temp {
  method: string;
  headers: Record<string, string>;
  body?: string;
}

interface UserData {
  [key: string]: unknown;
}

function request(method: string) {
  return (url: string, body?: object) => {
    const requestOptions: temp = {
      method,
      headers: authHeader(url)
    };
    if (body) {
      requestOptions.headers['Content-Type'] = 'application/json';
      requestOptions.body = JSON.stringify(body);
    }
    return fetch(url, requestOptions).then(handleResponse);
  };
}

// helper functions

function authHeader(url: string): Record<string, string> {
  // return auth header with jwt if user is logged in and request is to the api url
  const { user } = useAuthStore();
  const isLoggedIn = !!user?.token;
  const apiUrl = import.meta.env.VITE_API_URL || '';
  const isApiUrl = apiUrl ? url.startsWith(apiUrl) : url.startsWith('/');
  if (isLoggedIn && isApiUrl) {
    return { Authorization: `Bearer ${user.token}` };
  } else {
    return {};
  }
}

function handleResponse(response: Response): Promise<UserData> {
  return response.text().then((text: string) => {
    const data = text && JSON.parse(text);

    if (!response.ok) {
      const error = new Error(response.statusText);
      (error as any).response = response;
      throw error;
    }

    // Ensure data is of type UserData
    return data as UserData;
  });
}
