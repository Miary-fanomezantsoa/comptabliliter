<template>
  <div class="min-h-screen p-6 bg-gradient-to-br from-yellow-50 via-amber-100 to-amber-200 font-sans">
    <div class="max-w-7xl mx-auto space-y-8">

      <!-- Header -->
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-4xl font-bold text-amber-900">🍫 Gestion des factures</h2>
      </div>
    <!-- Filtre par date -->
<div class="flex flex-wrap gap-4 items-center bg-white p-4 rounded-lg shadow">
  <div>
    <label class="block text-sm font-medium text-amber-900">Date début</label>
    <input type="date" v-model="filterStart"
           class="border rounded-lg px-3 py-1 mt-1 focus:ring-amber-500" />
  </div>
  <div>
    <label class="block text-sm font-medium text-amber-900">Date fin</label>
    <input type="date" v-model="filterEnd"
           class="border rounded-lg px-3 py-1 mt-1 focus:ring-amber-500" />
  </div>
</div>
      <!-- Liste des factures -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  <div v-for="invoice in filteredInvoices" :key="invoice.id"
       @click="selectInvoice(invoice)"
       :class="{'border-amber-700 bg-amber-100 shadow-lg': selectedInvoice && selectedInvoice.id === invoice.id, 'border-transparent bg-white hover:bg-amber-50 shadow hover:shadow-md': true}"
       class="cursor-pointer border rounded-xl p-4 transition">
    <h3 class="font-semibold text-lg text-amber-800">#{{ invoice.invoice_number }}</h3>
    <p class="text-gray-700">{{ invoice.patern }}</p>
    <p class="mt-2 font-bold text-amber-900">{{ invoice.amount }} Ar</p>
    <p class="mt-1 text-sm text-gray-500">Status: {{ invoice.status }}</p>
  </div>
</div>

      <!-- Détail facture -->
      <div v-if="selectedInvoice" class="bg-white p-6 rounded-xl shadow-md space-y-6">
        <h3 class="text-2xl font-bold text-amber-900 mb-2">📄 Détails de la facture #{{ selectedInvoice.invoice_number }}</h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <p><strong>Client:</strong> {{ selectedInvoice.patern }}</p>
          <p><strong>Date:</strong> {{ selectedInvoice.date }}</p>
          <p><strong>Échéance:</strong> {{ selectedInvoice.due_date }}</p>
          <p><strong>Status:</strong> <span class="font-semibold text-amber-800">{{ selectedInvoice.status }}</span></p>
        </div>

        <!-- Items -->
        <div v-if="invoiceItems.length" class="mt-4">
          <h4 class="text-lg font-semibold text-amber-800 mb-2">Articles</h4>
          <div class="overflow-x-auto">
            <table class="min-w-full border border-gray-300 rounded-lg overflow-hidden">
              <thead class="bg-amber-700 text-white">
                <tr>
                  <th class="px-4 py-2 text-left">Produit</th>
                  <th class="px-4 py-2 text-center">Quantité</th>
                  <th class="px-4 py-2 text-right">Prix unitaire</th>
                  <th class="px-4 py-2 text-right">Total</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in invoiceItems" :key="item.id" class="even:bg-amber-50">
                  <td class="px-4 py-2">{{ item.product_name }}</td>
                  <td class="px-4 py-2 text-center">{{ item.quantity }}</td>
                  <td class="px-4 py-2 text-right">{{ item.unit_price }}</td>
                  <td class="px-4 py-2 text-right font-bold">{{ item.quantity * item.unit_price }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Paiements -->
        <div v-if="payments.length" class="mt-6">
          <h4 class="text-lg font-semibold text-amber-800 mb-2">💰 Paiements</h4>
          <div class="overflow-x-auto">
            <table class="min-w-full border border-gray-300 rounded-lg overflow-hidden">
              <thead class="bg-amber-700 text-white">
                <tr>
                  <th class="px-4 py-2">Montant</th>
                  <th class="px-4 py-2">Mode</th>
                  <th class="px-4 py-2">Description</th>
                  <th class="px-4 py-2">Date</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="p in payments" :key="p.id" class="even:bg-amber-50">
                  <td class="px-4 py-2 font-semibold text-amber-900">{{ p.amount }} Ar</td>
                  <td class="px-4 py-2">{{ p.mode }}</td>
                  <td class="px-4 py-2">{{ p.description }}</td>
                  <td class="px-4 py-2">{{ p.date }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Résumé -->
          <div class="mt-4 text-right text-amber-900 font-bold">
            <p>Total payé: {{ totalPaid }} Ar</p>
            <p>Reste à payer: {{ remainingAmount }} Ar</p>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import api from '../axios';

export default {
  data() {
    return {
      filterStart: "",
      filterEnd: "",
      invoices: [],
      selectedInvoice: null,
      invoiceItems: [],
      payments: [],
      clients: [],
    }
  },
  created() {
    this.fetchInvoices();
    this.fetchClients();
  },
  computed: {
  filteredInvoices() {
    if (!this.filterStart && !this.filterEnd) return this.invoices;

    const start = this.filterStart ? new Date(this.filterStart) : null;
    const end = this.filterEnd ? new Date(this.filterEnd) : null;

    return this.invoices.filter(inv => {
      const invDate = new Date(inv.date);
      if (start && invDate < start) return false;
      if (end && invDate > end) return false;
      return true;
    });
  },
    totalPaid() {
      return this.payments.reduce((sum, p) => sum + p.amount, 0);
    },
    remainingAmount() {
      return this.selectedInvoice ? this.selectedInvoice.amount - this.totalPaid : 0;
    }
  },
  methods: {
    async fetchInvoices() {
      const res = await api.get('/api/invoices/');
      this.invoices = res.data;
    },
    async fetchClients() {
      const res = await api.get('/api/partners/?is_client=true');
      this.clients = res.data;
    },
    selectInvoice(invoice) {
      this.selectedInvoice = invoice;
      api.get(`/api/invoice-items/?invoice=${invoice.id}`).then(res => {
        this.invoiceItems = res.data;
      });
      api.get(`/api/payments/?invoice=${invoice.id}`).then(res => {
        this.payments = res.data;
      });
    },
  }
}
</script>
