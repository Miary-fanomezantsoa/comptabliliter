<template>
  <div class="min-h-screen p-6 bg-gray-50 font-sans">
    <div class="max-w-7xl mx-auto space-y-6">

      <!-- Header commandes -->
      <div class="flex flex-col sm:flex-row justify-between items-center gap-4 bg-gradient-to-r from-orange-500 to-orange-600 p-6 rounded-xl shadow-lg text-white">
  <h2 class="text-3xl font-bold">🛒 Commandes</h2>
  <p class="text-lg opacity-90">Gestion des commandes et paiements</p>
</div>


      <!-- Liste des commandes -->
      <ul class="bg-white rounded-lg shadow divide-y divide-gray-200">
        <li v-for="order in orders" :key="order.id"
    @click="selectOrder(order)"
    :class="['cursor-pointer px-4 py-3 flex justify-between items-center rounded-lg transition', selectedOrder && selectedOrder.id === order.id ? 'bg-orange-200 shadow-md font-semibold' : 'hover:bg-orange-100']">
  <span>Commande #{{ order.id }} - {{ order.partner?.name || '-' }}</span>
  <span class="px-2 py-1 rounded-full text-sm font-medium"
        :class="order.status === 'paid' ? 'bg-green-200 text-green-800' : 'bg-yellow-200 text-yellow-800'">
    {{ statusLabel(order.status) }}
  </span>
</li>
      </ul>

      <!-- Détails commande -->
      <div v-if="selectedOrder" class="bg-white p-4 rounded-lg shadow space-y-4">
        <h2 class="text-xl font-semibold text-orange-900 text-center">Détails de la commande</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <p><strong>Client:</strong> {{ selectedOrder.partner?.name || '-' }}</p>
          <p><strong>Date:</strong> {{ selectedOrder.date }}</p>
          <p><strong>État:</strong></p>
          <select v-model="selectedOrder.status"
        @change="updateOrderStatus(selectedOrder)"
        class="border border-gray-300 rounded px-2 py-1 w-full">
  <option v-for="status in allowedStatuses(selectedOrder.status)" :key="status" :value="status">
    {{ statusLabel(status) }}
  </option>
</select>

        </div>

        <!-- Produits -->
        <div class="bg-white p-4 rounded-xl shadow-md">
  <h3 class="text-lg font-semibold text-orange-800 mb-3 border-b pb-2">Produits</h3>
  <table class="min-w-full table-auto border border-gray-200 rounded overflow-hidden">
    <thead class="bg-orange-700 text-white">
      <tr>
        <th class="px-4 py-2 text-left">Produit</th>
        <th class="px-4 py-2 text-left">Quantité</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="item in orderItems" :key="item.id" class="even:bg-orange-50 hover:bg-orange-100 transition-colors">
        <td class="px-4 py-2">{{ item.product }}</td>
        <td class="px-4 py-2">{{ item.quantity }}</td>
      </tr>
    </tbody>
  </table>
</div>

        <!-- Facturation -->
<div class="flex items-center gap-4 mt-4">
  <button @click="createInvoice"
          class="bg-green-600 text-white rounded px-4 py-2 hover:bg-green-700 transition">
    🧾 Facturer
  </button>
  <label class="flex items-center gap-2 text-gray-700">
    <input type="checkbox" v-model="exportPDF" class="w-4 h-4"/>
    Exporter en PDF
  </label>
</div>

        <!-- Paiements -->
        <div v-if="payments.length">
          <h3 class="text-lg font-semibold text-orange-800 mb-2">Paiements</h3>
          <table class="min-w-full table-auto border border-gray-300 rounded overflow-hidden">
            <thead class="bg-orange-700 text-white">
              <tr>
                <th class="px-4 py-2">Montant</th>
                <th class="px-4 py-2">Mode</th>
                <th class="px-4 py-2">Description</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="p in payments" :key="p.id" class="even:bg-orange-50">
                <td class="px-4 py-2">{{ p.amount }}</td>
                <td class="px-4 py-2">{{ p.mode }}</td>
                <td class="px-4 py-2">{{ p.description }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Ajouter un paiement -->
        <div class="space-y-2">
          <h3 class="text-lg font-semibold text-orange-800">Ajouter un paiement</h3>

          <div class="grid grid-cols-1 sm:grid-cols-4 gap-2">
          <p class="text-right font-semibold text-orange-700 mb-2">
  Reste à payer: {{ remainingAmount }} Ar
</p>
            <input type="number" v-model.number="newPayment.amount" placeholder="Montant"
                   class="border border-gray-300 rounded px-2 py-1 w-full"/>
            <select v-model="newPayment.mode" class="border border-gray-300 rounded px-2 py-1 w-full">
              <option disabled value="">Choisir un mode</option>
              <option value="Cash">Caisse directe</option>
              <option value="card">Carte bancaire</option>
              <option value="mvola">MVola</option>
              <option value="orange">Orange Money</option>
              <option value="airtel">Airtel Money</option>
              <option value="bank">Virement bancaire</option>
              <option value="cod">Paiement à la livraison</option>
            </select>
            <input type="text" v-model="newPayment.description" placeholder="Description"
                   class="border border-gray-300 rounded px-2 py-1 w-full"/>
            <button @click="addPayment"
                    class="bg-orange-600 text-white rounded px-4 py-1 hover:bg-orange-700 transition">Ajouter</button>
          </div>
        </div>
      </div>

      <!-- Nouvelle commande -->
      <div class="bg-white p-4 rounded-lg shadow space-y-4">
        <h2 class="text-xl font-semibold text-orange-900 text-center">Nouvelle commande</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <select v-model="newOrder.partner_id" class="border border-gray-300 rounded px-2 py-1 w-full">
            <option value="" disabled>Choisir un clients</option>
            <option v-for="c in clients" :key="c.id" :value="c.id">{{ c.name }}</option>
          </select>
        </div>

        <!-- Produits -->
        <div class="space-y-4 bg-white p-6 rounded-xl shadow-md">
  <h3 class="text-xl font-semibold text-orange-800 border-b pb-2 mb-4">Produits</h3>

  <div v-for="(item, index) in newOrderItems" :key="index" class="flex flex-wrap items-center gap-4 p-3 bg-gray-50 rounded-lg shadow-sm hover:shadow-md transition">

    <!-- Choix produit -->
    <select v-model="item.product_id" class="flex-1 border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500">
      <option value="" disabled>Choisir un produit</option>
      <option v-for="p in products" :key="p.id" :value="p.id">{{ p.name }} - {{ p.unit_price }} Ar</option>
    </select>

    <!-- Quantité -->
    <input type="number" v-model.number="item.quantity" min="1"
           class="w-24 border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500 text-center"
           placeholder="Qté"/>

    <!-- Supprimer -->
    <button @click="removeNewItem(index)"
            class="flex items-center gap-1 bg-red-600 text-white rounded-lg px-3 py-2 hover:bg-red-700 transition shadow-sm">
      🗑 Supprimer
    </button>

    <!-- Total -->
    <span class="font-semibold text-orange-700 ml-auto">Total: {{ itemTotal(item) }} Ar</span>
  </div>

  <!-- Ajouter produit -->
  <button @click="addNewItemLine"
          class="flex items-center gap-2 justify-center w-full bg-orange-600 text-white rounded-lg px-4 py-2 hover:bg-orange-700 transition shadow-md">
    ➕ Ajouter produit
  </button>

  <!-- Total commande -->
  <div class="flex justify-between items-center mt-4 p-4 bg-orange-50 rounded-lg shadow-inner">
    <span class="text-lg font-semibold text-orange-800">Total commande:</span>
    <span class="text-xl font-bold text-orange-900">{{ orderTotal }} Ar</span>
  </div>

  <!-- Créer commande -->
  <button @click="createOrder"
          class="w-full sm:w-auto flex justify-center bg-orange-600 text-white font-bold rounded-lg px-6 py-3 hover:bg-orange-700 transition shadow-lg">
    🛒 Créer commande
  </button>
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
      orders: [],
      exportPDF: false,
      selectedOrder: null,
      orderItems: [],
      payments: [],
      partners: [],
      products: [],

      newOrder: { partner_id: null },
      newOrderItems: [],
      newPayment: { amount: 0, mode: '', description: '' }
    };
  },
  created() {
    this.fetchOrders();
    this.fetchPartners();
    this.fetchProducts();
  },
  computed: {
   clients() {
    return this.partners.filter(p => p.is_client);
  },
  orderTotal() {
  let sum = 0;

  this.newOrderItems.forEach(item => {
    const product = this.products.find(p => p.id === item.product_id);
    const price = product ? Number(product.unit_price) : 0;
    const quantity = item.quantity ? Number(item.quantity) : 0;
    sum += price * quantity;
  });

  return sum;
},
selectedOrderTotal() {
    if (!this.selectedOrder) return 0;
    let sum = 0;
    this.orderItems.forEach(item => {
    const product = this.products.find(p => p.name === item.product);
      console.log("Produit:", product);
      const price = product ? Number(product.unit_price) : 0;
      console.log("price:", price);
      const quantity = item.quantity ? Number(item.quantity) : 0;
      sum += price * quantity;
    });
    return sum;
  },

  // Total payé pour la commande sélectionnéeconst res = await api.post('/api/invoice/', payload);
  selectedOrderPaid() {
    return this.payments.reduce((sum, p) => sum + Number(p.amount || 0), 0);
  },

  // Reste à payer pour la commande sélectionnée
  remainingAmount() {
    return this.selectedOrderTotal - this.selectedOrderPaid;
  },
  // Somme des paiements déjà faits pour la commande sélectionnée
  totalPaid() {
    return this.payments.reduce((sum, p) => sum + Number(p.amount || 0), 0);
  },
},
  methods: {
  allowedStatuses(currentStatus) {
    const orderFlow = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled'];
    const currentIndex = orderFlow.indexOf(currentStatus);
    if (currentIndex === -1) return orderFlow;
    return orderFlow.slice(currentIndex);
  },

  statusLabel(status) {
    const labels = {
      pending: 'En attente',
      confirmed: 'Confirmée',
      shipped: 'Expédiée',
      delivered: 'Livrée',
      cancelled: 'Annulée'
    };
    return labels[status] || status;
  },

  async updateOrderStatus(order) {
    try {
      const res = await api.patch(`/api/orders/${order.id}/`, {
        status: order.status
      });
      console.log("Statut mis à jour:", res.data);
    } catch (error) {
      console.error("Erreur mise à jour statut:", error.response?.data || error);
    }
  },

  async fetchOrders() {
    const res = await api.get('/api/orders/');
    this.orders = res.data;
  },

  async fetchPartners() {
    const res = await api.get('/api/partners/');
    this.partners = res.data;
  },

  async fetchProducts() {
    const res = await api.get('/api/products/');
    this.products = res.data;
  },


  addNewItemLine() {
    this.newOrderItems.push({ product_id: null, quantity: 1 });
  },

  removeNewItem(index) {
    this.newOrderItems.splice(index, 1);
  },

  itemTotal(item) {
    const product = this.products.find(p => p.id === item.product_id);
    const price = product ? Number(product.unit_price) : 0;
    const quantity = item.quantity ? Number(item.quantity) : 0;
    return price * quantity;
  },

  async createOrder() {
    if (!this.newOrder.partner_id || this.newOrderItems.length === 0) return;

    const validItems = this.newOrderItems
      .filter(i => i.product_id && i.quantity > 0)
      .map(i => ({ product_id: i.product_id, quantity: i.quantity }));

    if (!validItems.length) return;

    try {
      const res = await api.post('/api/orders/', {
        partner_id: this.newOrder.partner_id,
        items: validItems,
        date: new Date().toISOString().slice(0, 10)
      });
      this.orders.push(res.data);
      this.newOrder.partner_id = null;
      this.newOrderItems = [];
    } catch (error) {
      console.error("Erreur création commande:", error.response?.data || error);
    }
  },

async addPayment() {
  if (!this.selectedOrder || !this.selectedOrder.partner) return;

  let paymentAmount = Number(this.newPayment.amount);

  // Limiter le paiement au reste à payer
  if (paymentAmount > this.remainingAmount) {
    paymentAmount = this.remainingAmount;
    alert(`Le montant dépasse le reste à payer. Le paiement sera limité à ${paymentAmount} Ar.`);
    return;
  }

  if (paymentAmount <= 0) return;

  const partnerId = this.selectedOrder.partner?.id || this.selectedOrder.partner_id;

  const paymentData = {
    pattern_id: partnerId,
    amount: paymentAmount,
    mode: this.newPayment.mode,
    description: this.newPayment.description,
    date: new Date().toISOString().slice(0, 10),
    type: 'incoming',
    payment_number: `PAY-${Date.now()}`
  };

  try {
    const res = await api.post('/api/payments/', paymentData);
    this.payments.push(res.data);
    this.newPayment = { amount: 0, mode: '', description: '' };
  } catch (error) {
    console.error("Erreur ajout paiement:", error.response?.data || error);
  }
},


  async selectOrder(order) {
    this.selectedOrder = order;

    // Récupérer les items de la commande
    const resItems = await api.get(`/api/order-items/?order_id=${order.id}`);
    this.orderItems = resItems.data;

    // Trouver l'objet partenaire
    let partnerObj = null;
    if (order.partner?.id) {
      partnerObj = order.partner;
    } else if (order.partner_id) {
      partnerObj = this.partners.find(p => p.id === order.partner_id);
    } else {
      partnerObj = this.partners.find(p => p.name === order.partner);
    }

    if (partnerObj) {
      // Utiliser l'ID de partnerObj pour récupérer les paiements
      const resPayments = await api.get(`/api/payments/?pattern=${partnerObj.id}`);
      this.payments = resPayments.data;

      // Mettre à jour selectedOrder.partner pour avoir un objet complet
      this.selectedOrder.partner = partnerObj;
    } else {
      this.payments = [];
    }

    console.log("selectedOrder complet:", this.selectedOrder);
  },
async createInvoice() {
    if (!this.selectedOrder) return;

    const payload = {
      order_id: this.selectedOrder.id,
      export_pdf: this.exportPDF
    };

    try {
      const res = await api.post('/api/invoice/', payload, {
        responseType: this.exportPDF ? 'blob' : 'json'
      });

      if (this.exportPDF) {
        // Télécharger le PDF
        const blob = new Blob([res.data], { type: 'application/pdf' });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `facture_${this.selectedOrder.id}.pdf`);
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
      } else {
        alert("Facture générée !");
        console.log(res.data);
      }

    } catch (error) {
      console.error("Erreur création facture :", error.response?.data || error);
      alert("Erreur lors de la facturation.");
    }
  }




  }
}
</script>
