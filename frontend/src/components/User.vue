<script setup>
import { ref, onMounted } from 'vue'
import api from '../axios'

const users = ref([])

const form = ref({
  id: null,
  username: '',
  email: '',
  currentPassword: '',
  password: '',
  confirmPassword: '',
  role: 'comptable'
})

const isEditing = ref(false)
const showPassword = ref(false)

const fetchUsers = async () => {
  try {
    const res = await api.get('http://localhost:8000/api/users/')
    users.value = res.data
  } catch (err) {
    console.error(err)
  }
}

const saveUser = async () => {
  if (form.value.password !== form.value.confirmPassword) {
    alert("Les mots de passe ne correspondent pas !")
    return
  }

  if (isEditing.value && !form.value.currentPassword) {
    alert("Veuillez saisir le mot de passe actuel pour modifier l'utilisateur.")
    return
  }

  try {
    if (isEditing.value) {
      await api.put(`http://localhost:8000/api/users/${form.value.id}/`, form.value)
      isEditing.value = false
    } else {
      await api.post('http://localhost:8000/api/users/', form.value)
    }

    resetForm()
    fetchUsers()
  } catch (err) {
    console.error(err)
  }
}

const editUser = (user) => {
  form.value = { ...user, password: '', confirmPassword: '', currentPassword: '' }
  isEditing.value = true
}

const deleteUser = async (id) => {
  try {
    await api.delete(`http://localhost:8000/api/users/${id}/`)
    fetchUsers()
  } catch (err) {
    console.error(err)
  }
}

const resetForm = () => {
  form.value = { id: null, username: '', email: '', currentPassword: '', password: '', confirmPassword: '', role: 'comptable' }
  isEditing.value = false
}

onMounted(fetchUsers)
</script>

<template>
<div class="max-w-4xl mx-auto p-6 bg-white shadow rounded-lg">
  <h2 class="text-2xl sm:text-3xl font-bold mb-4 text-center">Gestion des utilisateurs</h2>

  <form @submit.prevent="saveUser" class="mb-6 grid grid-cols-1 sm:grid-cols-2 gap-4">
    <input v-model="form.username" placeholder="Username" class="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"/>
    <input v-model="form.email" placeholder="Email" type="email" class="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"/>

    <!-- Mot de passe actuel uniquement si édition -->
    <div v-if="isEditing" class="relative w-full">
      <input
        :type="showPassword ? 'text' : 'password'"
        v-model="form.currentPassword"
        placeholder="Mot de passe actuel"
        class="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 pr-10"/>
      <button type="button" @click="showPassword = !showPassword" class="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-500">
        {{ showPassword ? '🙈' : '👁️' }}
      </button>
    </div>

    <!-- Nouveau mot de passe -->
    <div class="relative w-full">
      <input
        :type="showPassword ? 'text' : 'password'"
        v-model="form.password"
        placeholder="Nouveau mot de passe"
        class="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 pr-10"/>
    </div>

    <!-- Confirmer mot de passe -->
    <div class="relative w-full">
      <input
        :type="showPassword ? 'text' : 'password'"
        v-model="form.confirmPassword"
        placeholder="Confirmer mot de passe"
        class="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 pr-10"/>
    </div>

    <select v-model="form.role" class="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
      <option value="comptable">Comptable</option>
      <option value="admin_comptable">Admin Comptable</option>
    </select>

    <div class="col-span-1 sm:col-span-2 flex gap-2">
      <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 flex-1">
        {{ isEditing ? 'Mettre à jour' : 'Créer utilisateur' }}
      </button>
      <button type="button" @click="resetForm" class="bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500 flex-1">
        Annuler
      </button>
    </div>
  </form>

  <div class="overflow-x-auto">
    <table class="w-full table-auto border-collapse border border-gray-200">
      <thead class="bg-gray-100">
        <tr>
          <th class="border px-4 py-2">Username</th>
          <th class="border px-4 py-2">Email</th>
          <th class="border px-4 py-2">Role</th>
          <th class="border px-4 py-2">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50">
          <td class="border px-4 py-2">{{ user.username }}</td>
          <td class="border px-4 py-2">{{ user.email }}</td>
          <td class="border px-4 py-2">{{ user.role }}</td>
          <td class="border px-4 py-2 flex flex-wrap gap-2">
            <button @click="editUser(user)" :disabled="user.is_superuser" class="bg-yellow-400 text-white px-2 py-1 rounded hover:bg-yellow-500">Éditer</button>
            <button @click="deleteUser(user.id)" :disabled="user.is_superuser" class="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600">Supprimer</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
</template>
