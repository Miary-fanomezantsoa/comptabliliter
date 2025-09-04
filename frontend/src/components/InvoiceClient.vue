<template>
  <div class="min-h-screen p-6 bg-gray-50 font-sans">
    <div class="max-w-7xl mx-auto space-y-6">

      <!-- Header -->
      <div class="flex justify-between items-center">
        <h2 class="text-3xl font-bold text-indigo-800">Gestion des factures</h2>
      </div>

      <!-- Liste des factures -->
      <div class="bg-white p-6 rounded-lg shadow space-y-4">
        <h3 class="text-xl font-semibold text-indigo-700">Factures existantes</h3>

        <ul class="divide-y divide-gray-200">
          <li v-for="invoice in invoices" :key="invoice.id"
              @click="selectInvoice(invoice)"
              :class="{'bg-indigo-100 font-semibold': selectedInvoice && selectedInvoice.id === invoice.id, 'cursor-pointer hover:bg-indigo-50': true}"
              class="px-4 py-3 flex justify-between items-center">
            <span>#{{ invoice.invoice_number }} - {{ invoice.patern }} - {{ invoice.status }}</span>
            <span>{{ invoice.amount }} Ar</span>
          </li>
        </ul>
      </div>

      <!-- Détail facture -->
      <div v-if="selectedInvoice" class="bg-white p-6 rounded-lg shadow space-y-4">
        <h3 class="text-xl font-semibold text-indigo-700">Détails de la facture #{{ selectedInvoice.invoice_number }}</h3>

        <p><strong>Client:</strong> {{ selectedInvoice.patern }}</p>
        <p><strong>Date:</strong> {{ selectedInvoice.date }}</p>
        <p><strong>Échéance:</strong> {{ selectedInvoice.due_date }}</p>
        <p><strong>Status:</strong> {{ selectedInvoice.status }}</p>

        <!-- Items -->
        <div v-if="invoiceItems.length">
          <h4 class="font-semibold text-gray-800 mb-2">Items</h4>
          <table class="min-w-full border border-gray-300 rounded overflow-hidden">
            <thead class="bg-indigo-700 text-white">
              <tr>
                <th class="px-4 py-2">Produit</th>
                <th class="px-4 py-2">Quantité</th>
                <th class="px-4 py-2">Prix unitaire</th>
                <th class="px-4 py-2">Total</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in invoiceItems" :key="item.id" class="even:bg-indigo-50">
                <td class="px-4 py-2">{{ item.product_name }}</td>
                <td class="px-4 py-2">{{ item.quantity }}</td>
                <td class="px-4 py-2">{{ item.unit_price }}</td>
                <td class="px-4 py-2">{{ item.quantity * item.unit_price }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import api from '../axios'; // ton axios configuré

export default {
  data() {
    return {
      invoices: [],
      selectedInvoice: null,
      invoiceItems: [],
      clients: [],
    }
  },
  created() {
    this.fetchInvoices();
    this.fetchClients();
  },
  computed: {
    invoiceTotal() {
      return this.newInvoice.items.reduce((sum, i) => sum + (i.quantity * i.unit_price || 0), 0);
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
    },
    addItem() {
      this.newInvoice.items.push({ product_name: '', quantity: 1, unit_price: 0 });
    },
    removeItem(index) {
      this.newInvoice.items.splice(index, 1);
    },
    itemTotal(item) {
      return item.quantity * item.unit_price;
    },
  }
}
</script>

<style scoped>
/* Scroll si nécessaire */
</style>
