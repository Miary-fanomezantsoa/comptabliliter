<template>
  <div class="flex-1 flex flex-col overflow-hidden p-8 bg-[#f7f1e1] min-h-screen">
    <!-- Titre -->
    <h1 class="text-4xl font-extrabold mb-10 text-[#5a3e36]">🍫 Tableau de bord Chocolaterie</h1>

    <!-- Cartes de stats -->
    <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
      <div
        v-for="stat in stats"
        :key="stat.title"
        :class="[
          'p-6 rounded-3xl shadow-md transform transition duration-300 hover:scale-105 hover:shadow-2xl',
          stat.color
        ]"
      >
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-lg font-semibold flex items-center gap-3 text-white">
            <span class="text-2xl">{{ stat.icon }}</span> {{ stat.title }}
          </h2>
          <span class="text-3xl font-bold text-white">{{ stat.value }}</span>
        </div>
        <p class="text-white/90 text-sm">{{ stat.label }}</p>
      </div>
    </section>

    <!-- Actions rapides -->
    <section>
      <h2 class="text-2xl font-bold text-[#5a3e36] mb-5">⚡ Actions rapides</h2>
      <div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <button
          v-for="action in actions"
          :key="action.label"
          @click="action.handler"
          class="flex items-center justify-center gap-2 bg-gradient-to-r from-[#8b4513] to-[#a0522d] text-white py-4 px-6 rounded-2xl shadow-md hover:scale-105 hover:shadow-xl transition-transform duration-300 font-medium text-sm"
        >
          <span class="text-lg">{{ action.icon }}</span>
          {{ action.label }}
        </button>
      </div>
    </section>
  </div>
</template>

<script>
import api from "../axios";

export default {
  name: "Dashboard",
  data() {
    return {
      stats: [
        { title: "Partenaires", value: 0, icon: "👥", label: "Nombre total de Partenaires", color: "bg-gradient-to-r from-[#d2b48c] to-[#c19a6b]" }, // Beige → Caramel
        { title: "Commandes", value: 0, icon: "🛒", label: "Commandes enregistrées", color: "bg-gradient-to-r from-[#8b4513] to-[#a0522d]" }, // Chocolat au lait
        { title: "Factures", value: 0, icon: "🧾", label: "Factures générées", color: "bg-gradient-to-r from-[#3e2c23] to-[#5a3e36]" }, // Chocolat noir
        { title: "Paiements", value: 0, icon: "💳", label: "Paiements reçus", color: "bg-gradient-to-r from-[#d2691e] to-[#ffb347]" }, // Caramel / Doré
      ],
      actions: [
        { label: "Créer une facture", icon: "📝", handler: () => this.$router.push("/commande&payment") },
        { label: "Ajouter un client", icon: "➕", handler: () => this.$router.push("/partners") },
        { label: "Voir le journal", icon: "📒", handler: () => this.$router.push("/journals") },
        { label: "Exporter PDF", icon: "📤", handler: () => alert("Exporter PDF") },
      ],
    };
  },
  mounted() {
    this.fetchStats();
  },
  methods: {
    async fetchStats() {
      try {
        const [clientsRes, ordersRes, invoicesRes, paymentsRes] = await Promise.all([
          api.get("/api/partners/"),
          api.get("/api/orders/"),
          api.get("/api/invoices/"),
          api.get("/api/payments/"),
        ]);

        this.stats[0].value = clientsRes.data.length;
        this.stats[1].value = ordersRes.data.length;
        this.stats[2].value = invoicesRes.data.length;
        this.stats[3].value = paymentsRes.data.length;
      } catch (error) {
        console.error("Erreur lors de la récupération des stats", error);
      }
    },
  },
};
</script>

<style scoped>
/* Optionnel : animations plus douces */
</style>
