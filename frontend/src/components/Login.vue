<template>
  <div class="login-container">
    <div class="login-logo">
      <img src="../../public/logo_rm_bg.png" alt="Chocolaterie Robert" />
      <h1>Chocolaterie Robert</h1>
    </div>

    <form @submit.prevent="login" class="login-form" :class="{ 'animate': loading }">
      <input
        v-model="username"
        placeholder="Nom d'utilisateur"
        required
        autocomplete="username"
        :disabled="loading"
      />
      <input
        type="password"
        v-model="password"
        placeholder="Mot de passe"
        required
        autocomplete="current-password"
        :disabled="loading"
      />
      <button type="submit" :disabled="loading">
        <span v-if="loading" class="loader"></span>
        <span v-else>Se connecter</span>
      </button>
      <p v-if="error" class="error-message">{{ error }}</p>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      username: '',
      password: '',
      error: null,
      loading: false,
    }
  },
  methods: {
    async login() {
      this.error = null
      this.loading = true
      try {
        const response = await axios.post('http://localhost:8000/api/token/', {
          username: this.username,
          password: this.password,
        })
        localStorage.setItem('access_token', response.data.access)
        localStorage.setItem('refresh_token', response.data.refresh)

        await this.fetchUser()
        this.$router.push({ name: 'Dashboard' })
      } catch (err) {
        this.error = "Nom d'utilisateur ou mot de passe incorrect"
      } finally {
        this.loading = false
      }
    },
    async fetchUser() {
      try {
        const token = localStorage.getItem('access_token')
        const response = await axios.get('http://localhost:8000/api/user/', {
          headers: { Authorization: `Bearer ${token}` },
        })
        console.log('Utilisateur connecté :', response.data)
      } catch {
        this.error = "Impossible de récupérer les infos utilisateur"
      }
    },
  },
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Pacifico&family=Roboto:wght@400;700&display=swap');

.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 30px 25px;
  box-shadow: 0 8px 25px rgba(0,0,0,0.2);
  border-radius: 15px;
  background: linear-gradient(135deg, #d2691e, #8b4513);
  font-family: 'Roboto', sans-serif;
  color: #fff;
  position: relative;
  overflow: hidden;
}

.login-logo {
  text-align: center;
  margin-bottom: 25px;
  animation: fadeInDown 1s ease;
}

.login-logo img {
  width: 70px;
  margin-bottom: 10px;
}

.login-logo h1 {
  font-family: 'Pacifico', cursive;
  font-size: 1.8rem;
  color: #fff8f0;
}

.login-form {
  display: flex;
  flex-direction: column;
  animation: fadeIn 1.2s ease;
}

input {
  padding: 12px 15px;
  margin-bottom: 15px;
  font-size: 16px;
  border-radius: 8px;
  border: none;
  outline: none;
  transition: all 0.3s ease;
  background-color: #fff3e0;
  color: #4b2e2b;
}

input:focus {
  box-shadow: 0 0 8px #8b4513;
}

button {
  padding: 12px;
  background: linear-gradient(145deg, #fff3e0, #d2691e);
  color: #4b2e2b;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

button:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(0,0,0,0.2);
}

button:disabled {
  background: #a0522d;
  cursor: not-allowed;
}

.loader {
  border: 3px solid #f3f3f3;
  border-top: 3px solid #4b2e2b;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  animation: spin 1s linear infinite;
  display: inline-block;
}

.error-message {
  color: #ffcccb;
  margin-top: 10px;
  text-align: center;
  font-weight: bold;
}

/* Animations */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeInDown {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
