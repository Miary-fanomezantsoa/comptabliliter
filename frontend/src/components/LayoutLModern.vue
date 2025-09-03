<template>
  <div class="flex flex-col min-h-screen">

    <div class="flex flex-1">
      <!-- Sidebar -->
      <aside class="bg-white p-4 flex flex-col gap-2 shadow-md max-h-full">
        <router-link
          v-for="link in navLinks"
          :key="link.to"
          :to="link.to"
          class="flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-300 transform hover:translate-x-2 hover:bg-gray-100"
          :class="{ 'bg-yellow-100 text-yellow-600 font-bold': $route.path === link.to }"
        >
          <span class="text-lg">
            <template v-if="link.iconIsImg">
              <img :src="link.icon" alt="" class="w-5 h-5"/>
            </template>
            <template v-else>
              {{ link.icon }}
            </template>
          </span>
          <span class="font-semibold transition-colors duration-300 hover:text-yellow-500">
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
import Footer from "@/components/Footer.vue";
import paramIcon from "../../public/paramettre.png";

export default {
  name: "LayoutLModern",
  components: { HeaderWithNav, Footer },
  data() {
    return {
      navLinks: [
        { to: "/dashboard", label: "Dashboard", icon: "🏠", iconIsImg: false },
        { to: "/comptes", label: "Comptes", icon: "💰", iconIsImg: false },
        { to: "/journals", label: "Journal", icon: "📒", iconIsImg: false },
        { to: "/partners-list", label: "Partenaires", icon: "🤝", iconIsImg: false },
        { to: "/commande&payment", label: "Commande & Paiement", icon: "🛒", iconIsImg: false },
        { to: "/balance", label: "Balance", icon: "📊", iconIsImg: false },
        { to: "/livre", label: "Livre comptable", icon: "📚", iconIsImg: false },
        { to: "/User", label: "Gérer les utilisateurs", icon: "👤", iconIsImg: false },
        { to: "/produit", label: "Produits", icon:"🍫 ", iconIsImg: false },
        { to: "/Paramettre", label: "Paramètres", icon: paramIcon, iconIsImg: true }
      ],
    };
  },
};
</script>
