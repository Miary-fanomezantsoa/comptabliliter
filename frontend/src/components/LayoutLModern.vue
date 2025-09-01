<template>
  <div class="flex flex-col h-screen">
    <!-- Header -->
    <HeaderWithNav />

    <div class="flex flex-1 overflow-hidden">
      <!-- Sidebar -->
      <aside class="bg-white w-64 p-4 flex flex-col gap-2 shadow-md">
        <router-link
          v-for="link in navLinks"
          :key="link.to"
          :to="link.to"
          class="flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-300 transform hover:translate-x-2 hover:bg-gray-100"
        >
          <span class="text-lg">{{ link.icon }}</span>
          <span class="font-semibold transition-colors duration-300 hover:text-yellow-300">
            {{ link.label }}
          </span>
        </router-link>
      </aside>

      <!-- Main content -->
      <main class="flex-1 bg-gray-100 p-6 overflow-auto">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
import HeaderWithNav from "@/components/Header.vue";

export default {
  name: "LayoutLModern",
  components: { HeaderWithNav },
  data() {
    return {
      navLinks: [
        { to: "/dashboard", label: "Dashboard", icon: "🏠" },
        { to: "/comptes", label: "Comptes", icon: "💰" },
        { to: "/journals", label: "Journal", icon: "📒" },
        { to: "/partners-list", label: "Partenaires", icon: "🤝" },
        { to: "/commande&payment", label: "Commande & Paiement", icon: "🛒" },
        { to: "/balance", label: "Balance", icon: "📊" },
        { to: "/livre", label: "Livre comptable", icon: "📚" },
      ],
    };
  },
};
</script>
