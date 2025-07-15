<template>
  <div class="login-wrapper" :class="themeClass">
    <div class="container" :class="{ 'right-panel-active': rightPanelActive }">
      <div class="form-container sign-up-container">
        <form @submit.prevent="onRegister">
          <h1>Crear cuenta</h1>
          <div v-if="registerError" class="error-message">
            {{ registerError }}
          </div>
          <input v-model="registerUsername" type="text" placeholder="Nombre" />
          <input v-model="registerEmail" type="email" placeholder="Email" />
          <input v-model="registerPassword" type="password" placeholder="Contraseña" style="margin-bottom: 20px" />
          <input v-model="registerConfirmPassword" type="password" placeholder="Confirmar Contraseña" style="margin-bottom: 20px" />
          <button type="submit" :disabled="registerLoading">
            {{ registerLoading ? 'Registrando...' : 'Registrarse' }}
          </button>
        </form>
      </div>
      <div class="form-container sign-in-container">
        <form @submit.prevent="onLogin">
          <h1>Iniciar sesión</h1>
          <div v-if="loginError" class="error-message">
            {{ loginError }}
          </div>
          <input v-model="loginField" type="text" placeholder="Nombre de usuario" />
          <input v-model="loginPassword" type="password" placeholder="Contraseña" style="margin-bottom: 20px" />
          <!-- <a href="#">¿Olvidó su contraseña?</a> -->
          <button type="submit" :disabled="loginLoading">
            {{ loginLoading ? 'Iniciando...' : 'Iniciar sesión' }}
          </button>
        </form>
      </div>
      <div class="overlay-container">
        <div class="overlay">
          <div class="overlay-panel overlay-left">
            <h1>¡Bienvenido de nuevo!</h1>
            <p>Para mantenerse conectado con nosotros inicie sesión con sus detalles personales</p>
            <button class="ghost" @click="showSignIn">Iniciar sesión</button>
          </div>
          <div class="overlay-panel overlay-right">
            <h1>¿Nueva cuenta?</h1>
            <p>Introduza sus detalles personales para comenzar la aventura con nosotros</p>
            <button class="ghost" @click="showSignUp">Registrarse</button>
          </div>
        </div>
      </div>
    </div>
    <footer>
      <p>Pablo Peramato Benito &copy; 2025</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useTheme } from 'vuetify';

const rightPanelActive = ref(false);
const theme = useTheme();

// Computed property mejorado para detectar el tema
const themeClass = computed(() => {
  const isDark = theme.global.current.value.dark;
  return isDark ? 'theme-dark' : 'theme-light';
});

const loginField = ref('');
const loginPassword = ref('');
const loginError = ref('');
const loginLoading = ref(false);

const registerEmail = ref('');
const registerUsername = ref('');
const registerPassword = ref('');
const registerConfirmPassword = ref('');
const registerError = ref('');
const registerLoading = ref(false);

const authStore = useAuthStore();

function showSignUp() {
  rightPanelActive.value = true;
}
function showSignIn() {
  rightPanelActive.value = false;
}

async function onLogin() {
  loginError.value = '';
  loginLoading.value = true;

  try {
    await authStore.login(loginField.value, loginPassword.value);
  } catch (err) {
    console.error(err);

    const errorString = String(err);

    if (errorString === 'Unauthorized' || errorString.includes('401')) {
      loginError.value = 'Contraseña incorrecta';
    } else if (errorString === 'Not Found' || errorString.includes('404')) {
      loginError.value = 'Usuario no encontrado';
    } else if (errorString.includes('500') || errorString.includes('Internal Server Error')) {
      loginError.value = 'Error interno del servidor. Inténtelo más tarde.';
    } else if (errorString.includes('network') || errorString.includes('Network')) {
      loginError.value = 'Error de red. Verifica tu conexión';
    } else {
      loginError.value = 'Error de autenticación. Verifica tus credenciales.';
    }
  } finally {
    loginLoading.value = false;
  }
}

async function onRegister() {
  registerError.value = '';
  registerLoading.value = true;

  try {
    await authStore.register(registerEmail.value, registerUsername.value, registerPassword.value, registerConfirmPassword.value);
    rightPanelActive.value = false;
  } catch (err) {
    console.error(err);

    const errorString = String(err);
    console.log('Error de registro:', errorString);

    if (errorString.includes('409') || errorString.includes('Conflict')) {
      registerError.value = 'El usuario o email ya existe';
    } else if (errorString.includes('400') || errorString.includes('Bad Request')) {
      registerError.value = 'Datos inválidos. Verifica la información';
    } else if (errorString.includes('500') || errorString.includes('Internal Server Error')) {
      registerError.value = 'Error del servidor. Inténtalo más tarde';
    } else {
      registerError.value = 'Error en el registro. Verifica los datos.';
    }
  } finally {
    registerLoading.value = false;
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css?family=Montserrat:400,800');

/* Wrapper principal que controla todo el tema */
.login-wrapper {
  min-height: 100vh;
  width: 100%;
  position: relative;
}

/* Tema claro (por defecto) */
.theme-light {
  --login-bg-primary: #1cbc94;
  --login-bg-secondary: #16a085;
  --login-surface: #ffffff;
  --login-text-primary: #212121;
  --login-text-secondary: #616161;
  --login-input-bg: #eeeeee;
  --login-border: #d0d0d0;
  --login-container-bg: #f6f5f7;
  --login-footer-bg: #222222;
  --login-error-bg: #f8d7da;
  --login-error-text: #721c24;
  --login-error-border: #f5c6cb;

  background: #f6f5f7;
}

/* Tema oscuro */
.theme-dark {
  --login-bg-primary: #1cbc94;
  --login-bg-secondary: #16a085;
  --login-surface: #2a2a2a;
  --login-text-primary: #ffffff;
  --login-text-secondary: #b0b0b0;
  --login-input-bg: #404040;
  --login-border: #606060;
  --login-container-bg: #1a1a1a;
  --login-footer-bg: #1a1a1a;
  --login-error-bg: #3f1a1a;
  --login-error-text: #ffffff;
  --login-error-border: #606060;

  background: #1a1a1a;
}

* {
  box-sizing: border-box;
}

.login-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  font-family: 'Montserrat', sans-serif;
  margin: -20px 0 50px;
}

h1 {
  font-weight: bold;
  margin: 0;
  color: var(--login-text-primary);
}

h2 {
  text-align: center;
  color: var(--login-text-primary);
}

p {
  font-size: 14px;
  font-weight: 100;
  line-height: 20px;
  letter-spacing: 0.5px;
  margin: 20px 0 30px;
  color: var(--login-text-secondary);
}

span {
  font-size: 12px;
  color: var(--login-text-secondary);
}

a {
  color: var(--login-text-primary);
  font-size: 14px;
  text-decoration: none;
  margin: 15px 0;
}

button {
  border-radius: 20px;
  border: 1px solid var(--login-bg-primary);
  background-color: var(--login-bg-primary);
  color: #ffffff;
  font-size: 12px;
  font-weight: bold;
  padding: 12px 45px;
  letter-spacing: 1px;
  text-transform: uppercase;
  transition: transform 80ms ease-in;
}

button:active {
  transform: scale(0.95);
}

button:focus {
  outline: none;
}

button.ghost {
  background-color: transparent;
  border-color: #ffffff;
}

form {
  background-color: var(--login-surface);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 0 50px;
  height: 100%;
  text-align: center;
}

input {
  background-color: var(--login-input-bg);
  border: none;
  padding: 12px 15px;
  margin: 8px 0;
  width: 100%;
  color: var(--login-text-primary);
  border-radius: 4px;
}

input::placeholder {
  color: var(--login-text-secondary);
}

.container {
  background-color: var(--login-surface);
  border-radius: 10px;
  box-shadow:
    0 14px 28px rgba(0, 0, 0, 0.25),
    0 10px 10px rgba(0, 0, 0, 0.22);
  position: relative;
  overflow: hidden;
  width: 768px;
  max-width: 100%;
  min-height: 480px;
  margin: auto;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.form-container {
  position: absolute;
  top: 0;
  height: 100%;
  transition: all 0.6s ease-in-out;
}

.sign-in-container {
  left: 0;
  width: 50%;
  z-index: 2;
}

.container.right-panel-active .sign-in-container {
  transform: translateX(100%);
}

.sign-up-container {
  left: 0;
  width: 50%;
  opacity: 0;
  z-index: 1;
}

.container.right-panel-active .sign-up-container {
  transform: translateX(100%);
  opacity: 1;
  z-index: 5;
  animation: show 0.6s;
}

@keyframes show {
  0%,
  49.99% {
    opacity: 0;
    z-index: 1;
  }

  50%,
  100% {
    opacity: 1;
    z-index: 5;
  }
}

.overlay-container {
  position: absolute;
  top: 0;
  left: 50%;
  width: 50%;
  height: 100%;
  overflow: hidden;
  transition: transform 0.6s ease-in-out;
  z-index: 100;
}

.container.right-panel-active .overlay-container {
  transform: translateX(-100%);
}

.overlay {
  background: var(--login-bg-primary);
  background: -webkit-linear-gradient(to right, var(--login-bg-primary), var(--login-bg-secondary));
  background: linear-gradient(to right, var(--login-bg-primary), var(--login-bg-secondary));
  background-repeat: no-repeat;
  background-size: cover;
  background-position: 0 0;
  color: #ffffff;
  position: relative;
  left: -100%;
  height: 100%;
  width: 200%;
  transform: translateX(0);
  transition: transform 0.6s ease-in-out;
}

.container.right-panel-active .overlay {
  transform: translateX(50%);
}

.overlay-panel {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 0 40px;
  text-align: center;
  top: 0;
  height: 100%;
  width: 50%;
  transform: translateX(0);
  transition: transform 0.6s ease-in-out;
}

/* Texto del overlay siempre blanco para mejor contraste sobre fondo verde */
.overlay-panel p,
.overlay-panel h1 {
  color: #ffffff !important;
}

.overlay-left {
  transform: translateX(-20%);
}

.container.right-panel-active .overlay-left {
  transform: translateX(0);
}

.overlay-right {
  right: 0;
  transform: translateX(0);
}

.container.right-panel-active .overlay-right {
  transform: translateX(20%);
}

.social-container {
  margin: 20px 0;
}

.social-container a {
  border: 1px solid var(--login-border);
  border-radius: 50%;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  margin: 0 5px;
  height: 40px;
  width: 40px;
}

.error-message {
  background-color: var(--login-error-bg);
  color: var(--login-error-text);
  border: 1px solid var(--login-error-border);
  border-radius: 4px;
  padding: 8px 12px;
  margin: 8px 0;
  font-size: 14px;
  width: 100%;
  text-align: center;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

button:disabled:active {
  transform: none;
}

footer {
  background-color: var(--login-footer-bg);
  color: #fff;
  font-size: 14px;
  bottom: 0;
  position: fixed;
  left: 0;
  right: 0;
  text-align: center;
  z-index: 999;
}

footer p {
  margin: 10px 0;
}

footer i {
  color: red;
}

footer a {
  color: #3c97bf;
  text-decoration: none;
}
</style>
