<script setup>
import { ref, onMounted , computed } from 'vue'
import api from '../axios'
import { UserPlus, X, Edit, Trash2, Eye, EyeOff } from 'lucide-vue-next';
const users = ref([])
const searchQuery = ref('')
const showForm = ref(false)

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
    showForm.value = false // Masquer le formulaire après sauvegarde
  } catch (err) {
    console.error(err)
  }
}

const editUser = (user) => {
  form.value = { ...user, password: '', confirmPassword: '', currentPassword: '' }
  isEditing.value = true
  showForm.value = true
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

const filteredUsers = computed(() => {
  const query = searchQuery.value.toLowerCase()
  return users.value.filter(u =>
    u.username.toLowerCase().includes(query) ||
    u.email.toLowerCase().includes(query)
  )
})

onMounted(fetchUsers)
</script>

<template>
<div class="min-h-screen p-6 bg-gradient-to-br from-yellow-50 via-amber-100 to-amber-200 font-sans rounded-lg shadow-inner">
  <div class="max-w-4xl mx-auto bg-white p-6 rounded-xl shadow-lg space-y-6 border border-amber-200">
    <h2 class="text-3xl font-bold text-center text-amber-900">Gestion des utilisateurs</h2>

    <!-- Bouton Ajouter utilisateur -->
    <button @click="showForm = !showForm"
        class="px-4 py-2 bg-amber-700 text-white rounded-lg hover:bg-amber-800 transition flex items-center gap-2">
  <component :is="showForm ? X : UserPlus" class="w-5 h-5"/>
  {{ showForm ? 'Annuler' : 'Ajouter utilisateur' }}
</button>


    <!-- Formulaire -->
    <form v-if="showForm" @submit.prevent="saveUser" class="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-4">
      <input v-model="form.username" placeholder="Username" class="w-full border border-amber-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-amber-500"/>
      <input v-model="form.email" placeholder="Email" type="email" class="w-full border border-amber-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-amber-500"/>

      <div v-if="isEditing" class="relative w-full">
        <input :type="showPassword ? 'text' : 'password'" v-model="form.currentPassword" placeholder="Mot de passe actuel"
          class="w-full border border-amber-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-amber-500 pr-10"/>
        <button type="button" @click="showPassword = !showPassword" class="absolute right-2 top-1/2 transform -translate-y-1/2 text-amber-600">
  <component :is="showPassword ? EyeOff : Eye" class="w-5 h-5"/>
</button>
      </div>

      <div class="relative w-full">
        <input :type="showPassword ? 'text' : 'password'" v-model="form.password" placeholder="Nouveau mot de passe"
          class="w-full border border-amber-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-amber-500 pr-10"/>
      </div>

      <div class="relative w-full">
        <input :type="showPassword ? 'text' : 'password'" v-model="form.confirmPassword" placeholder="Confirmer mot de passe"
          class="w-full border border-amber-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-amber-500 pr-10"/>
      </div>

      <select v-model="form.role" class="w-full border border-amber-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-amber-500">
        <option value="comptable">Comptable</option>
        <option value="admin_comptable">Admin Comptable</option>
      </select>

      <div class="col-span-1 sm:col-span-2 flex gap-2">
        <button type="submit" class="bg-amber-700 text-white px-4 py-2 rounded hover:bg-amber-800 flex-1">
          {{ isEditing ? 'Mettre à jour' : 'Créer utilisateur' }}
        </button>
        <button type="button" @click="resetForm" class="bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500 flex-1">
          Réinitialiser
        </button>
      </div>
    </form>

    <!-- Recherche -->
    <div class="relative mt-4 w-full">
  <input v-model="searchQuery" type="text" placeholder="Rechercher par username ou email"
         class="w-full border border-amber-300 rounded-lg p-2 pl-10 focus:ring focus:ring-amber-400"/>
  <Search class="w-5 h-5 absolute left-2 top-1/2 transform -translate-y-1/2 text-amber-500"/>
</div>

    <!-- Liste utilisateurs -->
    <div class="overflow-x-auto">
      <table class="w-full table-auto border-collapse border border-amber-200 mt-2 rounded-lg overflow-hidden shadow">
        <thead class="bg-amber-700 text-white">
          <tr>
            <th class="border px-4 py-2">Username</th>
            <th class="border px-4 py-2">Email</th>
            <th class="border px-4 py-2">Role</th>
            <th class="border px-4 py-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in filteredUsers" :key="user.id" class="even:bg-amber-50 hover:bg-amber-100">
            <td class="border px-4 py-2">{{ user.username }}</td>
            <td class="border px-4 py-2">{{ user.email }}</td>
            <td class="border px-4 py-2">{{ user.role }}</td>
            <td class="border px-4 py-2 flex flex-wrap gap-2">
  <button @click="editUser(user)" :disabled="user.is_superuser"
          class="bg-yellow-500 text-white p-2 rounded hover:bg-yellow-600 flex items-center justify-center">
    <Edit class="w-4 h-4"/>
  </button>
  <button @click="deleteUser(user.id)" :disabled="user.is_superuser"
          class="bg-red-600 text-white p-2 rounded hover:bg-red-700 flex items-center justify-center">
    <Trash2 class="w-4 h-4"/>
  </button>
</td>

          </tr>
        </tbody>
      </table>
    </div>
  </div>
</div>
</template>
