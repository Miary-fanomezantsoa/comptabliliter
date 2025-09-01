<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-orange-200 to-orange-400 p-4">
    <div class="w-full max-w-md bg-white rounded-xl shadow-2xl p-8 relative overflow-hidden">
      <!-- Logo -->
      <div class="text-center mb-6 animate-fadeInDown">
        <img src="../../public/logo_rm_bg.png" alt="Chocolaterie Robert" class="w-20 mx-auto mb-2" />
        <h1 class="text-3xl font-pacifico text-orange-800">Chocolaterie Robert</h1>
      </div>

      <!-- Formulaire -->
      <form @submit.prevent="login" class="space-y-4" :class="{ 'opacity-50 pointer-events-none': loading }">
        <input
          v-model="username"
          placeholder="Nom d'utilisateur"
          required
          autocomplete="username"
          class="w-full px-4 py-2 rounded-lg border border-orange-300 focus:ring-2 focus:ring-orange-500 focus:outline-none text-gray-800"
        />

        <!-- Champ mot de passe avec œil -->
        <div class="relative">
          <input
            :type="showPassword ? 'text' : 'password'"
            v-model="password"
            placeholder="Mot de passe"
            required
            autocomplete="current-password"
            class="w-full px-4 py-2 rounded-lg border border-orange-300 focus:ring-2 focus:ring-orange-500 focus:outline-none text-gray-800 pr-10"
          />
          <button
            type="button"
            @click="showPassword = !showPassword"
            class="absolute inset-y-0 right-2 flex items-center text-gray-600 hover:text-gray-900"
          >
            <span v-if="showPassword">👁️</span>
            <span v-else>🙈</span>
          </button>
        </div>

        <button
          type="submit"
          class="w-full bg-gradient-to-r from-orange-400 to-orange-600 text-white font-bold py-2 rounded-lg shadow-md hover:shadow-lg transition transform hover:-translate-y-1"
          :disabled="loading"
        >
          <span v-if="loading" class="loader mx-auto"></span>
          <span v-else>Se connecter</span>
        </button>
      </form>

      <p v-if="error" class="text-red-600 font-semibold mt-4 text-center">{{ error }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      username: '',
      password: '',
      showPassword: false, // <-- pour l’œil
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
