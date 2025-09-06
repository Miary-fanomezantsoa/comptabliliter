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
          <!-- Vérifie si c’est une image ou une icône Vue -->
          <template v-if="link.iconIsImg">
            <img :src="link.icon" alt="" class="w-5 h-5" />
          </template>
          <template v-else>
            <!-- ici on utilise le composant directement -->
            <component :is="link.icon" class="w-5 h-5" />
          </template>

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

import { Home, Wallet, BookOpen,MessageCircle, Handshake, ShoppingCart, BarChart, Book, User, Package, FileText, Settings ,Grid} from "lucide-vue-next"

export default {
  name: "LayoutLModern",
  components: {
    HeaderWithNav,
    Footer,
  },
  data() {
    return {
        navLinks: [
        { to: "/dashboard", label: "Dashboard", icon:Grid},
        { to: "/comptes", label: "Comptes", icon: Wallet },
        { to: "/journals", label: "Journal", icon: BookOpen },
        { to: "/partners-list", label: "Partenaires", icon: Handshake },
        { to: "/commande&payment", label: "Commande & Paiement", icon: ShoppingCart },
        { to: "/balance", label: "Balance", icon: BarChart },
        { to: "/livre", label: "Livre comptable", icon: Book },
        { to: "/User", label: "Gérer les utilisateurs", icon: User },
        { to: "/produit", label: "Produits", icon: Package },
        { to: "/invoice", label: "Invoice", icon: FileText },
        { to: "/Paramettre", label: "Paramètres", icon: Settings },
        { to: "/chatbot", label: "chatbot", icon: MessageCircle},


      ],
    };
  },
};
</script>
