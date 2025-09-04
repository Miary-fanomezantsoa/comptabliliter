<template>
  <header class="bg-gradient-to-r from-[#4d3a33] to-[#795548] h-16 flex items-center justify-between px-6 shadow-lg sticky top-0 z-50">
    <!-- Logo et titre -->
    <div class="flex items-center gap-3">
      <img src="/logo_rm_bg.png" alt="Logo" class="h-10 w-10 rounded-full shadow-md transition-transform duration-500 hover:scale-110 hover:-rotate-3"/>
      <span class="text-white text-xl font-bold select-none">Chocolaterie Robert</span>
    </div>

    <!-- Notifications et Déconnexion -->
    <div class="flex items-center gap-4">
      <!-- Icone notification -->
      <div class="relative">
        <button @click="toggleDropdown"
                class="text-white text-2xl hover:text-yellow-300 transition-colors">
          🔔
        </button>
        <!-- Badge nombre de notifications -->
        <span v-if="unreadCount"
              class="absolute -top-2 -right-2 bg-red-600 text-white text-xs font-bold px-2 py-0.5 rounded-full">
          {{ unreadCount }}
        </span>

        <!-- Dropdown des notifications -->
        <div v-if="showDropdown" class="absolute right-0 mt-2 w-72 bg-white shadow-lg rounded-lg overflow-hidden z-50">
          <div v-for="notif in notifications" :key="notif.id" class="p-2 border-b last:border-none">
            <span :class="notif.typeClass">{{ notif.message }}</span>
          </div>
          <div v-if="!notifications.length" class="p-2 text-gray-500 text-sm">Aucune notification</div>
        </div>
      </div>

      <!-- Bouton Déconnexion -->
      <button @click="logout"
              class="bg-[#c06b3e] text-white px-4 py-2 rounded-xl font-semibold shadow-lg hover:bg-[#a0522d] hover:shadow-xl transition duration-300 transform hover:scale-105">
        🔒 Se déconnecter
      </button>
    </div>
  </header>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import api from '../axios'; // Ton instance Axios configurée

export default {
  name: "HeaderWithNav",
  setup() {
    const notifications = ref([]);
    const showDropdown = ref(false);

    const toggleDropdown = () => showDropdown.value = !showDropdown.value;

    const fetchNotifications = async () => {
      try {
        const res = await api.get('/api/notifications/');
        notifications.value = res.data.map(n => ({
          ...n,
          typeClass: n.type === 'warning' ? 'text-orange-600' :
                     n.type === 'error' ? 'text-red-600' : 'text-blue-600'
        }));
      } catch (e) {
        console.error(e);
      }
    };

    onMounted(() => {
      fetchNotifications();
      // Optionnel : auto-refresh toutes les 30s
      setInterval(fetchNotifications, 30000);
    });

    const unreadCount = computed(() => notifications.value.length);

    const logout = () => {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      window.location.href = "/login"; // ou this.$router.push si tu utilises Vue Router
    };

    return { notifications, showDropdown, toggleDropdown, unreadCount, logout };
  }
};
</script>

<style scoped>
/* Ajustement du dropdown */
.relative > .absolute {
  max-height: 300px;
  overflow-y: auto;
}
</style>
