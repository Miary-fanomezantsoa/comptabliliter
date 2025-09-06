<template>
  <div class="flex-1 flex flex-col overflow-hidden p-8 bg-[#f7f1e1] min-h-screen">

    <!-- Titre -->
    <h1 class="text-4xl font-extrabold mb-10 text-[#5a3e36] flex items-center gap-3">
      <Package class="w-10 h-10 text-[#5a3e36]" /> Tableau de bord Chocolaterie
    </h1>

    <!-- Cartes de stats
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
            <component :is="stat.icon" class="w-7 h-7" /> {{ stat.title }}
          </h2>
          <span class="text-3xl font-bold text-white">{{ stat.value }}</span>
        </div>
        <p class="text-white/90 text-sm">{{ stat.label }}</p>
      </div>
    </section>
-->
    <!-- Graphiques -->
    <section class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
      <!-- Commandes -->
      <div>
        <h2 class="text-2xl font-bold text-[#5a3e36] mb-5 flex items-center gap-2">
          <ShoppingCart class="w-6 h-6 text-[#5a3e36]" /> Commandes par mois
        </h2>
        <OrdersChart :orders="orders" />
      </div>

      <!-- Factures -->
      <div>
        <h2 class="text-2xl font-bold text-[#5a3e36] mb-5 flex items-center gap-2">
          <FileText class="w-6 h-6 text-[#5a3e36]" /> Factures par mois
        </h2>
        <StatsChart
          :labels="months"
          :data="invoicesData"
          type="line"
          label="Factures"
          color="#3e2c23"
        />
      </div>

      <!-- Paiements -->
      <div>
        <h2 class="text-2xl font-bold text-[#5a3e36] mb-5 flex items-center gap-2">
          <CreditCard class="w-6 h-6 text-[#5a3e36]" /> Paiements par mois
        </h2>
        <StatsChart
          :labels="months"
          :data="paymentsData"
          type="line"
          label="Paiements"
          color="#d2691e"
        />
      </div>

      <!-- Partenaires -->
      <div>
        <h2 class="text-2xl font-bold text-[#5a3e36] mb-5 flex items-center gap-2">
          <Users class="w-6 h-6 text-[#5a3e36]" /> Partenaires
        </h2>
        <StatsChart
          :labels="months"
          :data="partnersData"
          type="bar"
          label="Partenaires"
          color="#d2b48c"
        />
      </div>
    </section>

    <!-- Actions rapides -->
    <section>
      <h2 class="text-2xl font-bold text-[#5a3e36] mb-5 flex items-center gap-2">
        <Zap class="w-6 h-6 text-[#5a3e36]" /> Actions rapides
      </h2>
      <div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <button
          v-for="action in actions"
          :key="action.label"
          @click="action.handler"
          class="flex items-center justify-center gap-2 bg-gradient-to-r from-[#8b4513] to-[#a0522d] text-white py-4 px-6 rounded-2xl shadow-md hover:scale-105 hover:shadow-xl transition-transform duration-300 font-medium text-sm"
        >
          <component :is="action.icon" class="w-5 h-5" /> {{ action.label }}
        </button>
      </div>
    </section>

  </div>
</template>

<script>
import api from "../axios";
import OrdersChart from "../components/OrdersChart.vue";
import StatsChart from "../components/StatsChart.vue";

// Lucide Icons
import { Users, ShoppingCart, FileText, CreditCard, Edit, Plus, BookOpen, Upload, Package, Zap } from "lucide-vue-next";

export default {
  name: "Dashboard",
  components: { OrdersChart, StatsChart, Users, ShoppingCart, FileText, CreditCard, Edit, Plus, BookOpen, Upload, Package, Zap },
  data() {
    return {
      orders: [],
      invoices: [],
      payments: [],
      partners: [],
      months: [...Array(12)].map((_, i) => `Mois ${i + 1}`),
      invoicesData: Array(12).fill(0),
      paymentsData: Array(12).fill(0),
      partnersData: Array(12).fill(0),
      stats: [
        { title: "Partenaires", value: 0, icon: Users, label: "Nombre total de Partenaires", color: "bg-gradient-to-r from-[#d2b48c] to-[#c19a6b]" },
        { title: "Commandes", value: 0, icon: ShoppingCart, label: "Commandes enregistrées", color: "bg-gradient-to-r from-[#8b4513] to-[#a0522d]" },
        { title: "Factures", value: 0, icon: FileText, label: "Factures générées", color: "bg-gradient-to-r from-[#3e2c23] to-[#5a3e36]" },
        { title: "Paiements", value: 0, icon: CreditCard, label: "Paiements reçus", color: "bg-gradient-to-r from-[#d2691e] to-[#ffb347]" },
      ],
      actions: [
        { label: "Créer une facture", icon: Edit, handler: () => this.$router.push("/commande&payment") },
        { label: "Ajouter un client", icon: Plus, handler: () => this.$router.push("/partners") },
        { label: "Voir le journal", icon: BookOpen, handler: () => this.$router.push("/journals") },
        { label: "Exporter PDF", icon: Upload, handler: () => alert("Exporter PDF") },
      ],
    };
  },
  mounted() {
    this.fetchStats();
    this.fetchOrders();
    this.fetchInvoices();
    this.fetchPayments();
    this.fetchPartners();
  },
  methods: {
    async fetchOrders() {
      try {
        const res = await api.get("/api/orders/");
        this.orders = res.data;
      } catch (err) {
        console.error("Erreur fetch orders", err);
      }
    },
    async fetchInvoices() {
      try {
        const res = await api.get("/api/invoices/");
        this.invoices = res.data;
        this.invoices.forEach(inv => {
          const month = new Date(inv.date).getMonth();
          this.invoicesData[month]++;
        });
      } catch (err) {
        console.error("Erreur fetch invoices", err);
      }
    },
    async fetchPayments() {
      try {
        const res = await api.get("/api/payments/");
        this.payments = res.data;
        this.payments.forEach(p => {
          const month = new Date(p.date).getMonth();
          this.paymentsData[month]++;
        });
      } catch (err) {
        console.error("Erreur fetch payments", err);
      }
    },
    async fetchPartners() {
      try {
        const res = await api.get("/api/partners/");
        this.partners = res.data;
        this.partners.forEach(p => {
          const month = new Date(p.created_at).getMonth();
          this.partnersData[month]++;
        });
      } catch (err) {
        console.error("Erreur fetch partners", err);
      }
    },
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
