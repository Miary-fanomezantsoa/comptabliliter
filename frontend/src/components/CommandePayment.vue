<template>
  <div>
    <h2>Commandes</h2>
    <ul>
      <li v-for="order in orders" :key="order.id"
          @click="selectOrder(order)"
          :class="{ selected: selectedOrder && selectedOrder.id === order.id }">
        Commande #{{ order.id }} - {{ order.partner }} - {{ order.status }}
      </li>
    </ul>

    <h2>Détails de la commande</h2>
    <div v-if="selectedOrder">
      <p><strong>Client:</strong> {{ selectedOrder.partner }}</p>
      <p><strong>Date:</strong> {{ selectedOrder.date }}</p>
      <p><strong>État:</strong> {{ selectedOrder.status }}</p>

      <h3>Produits</h3>
      <table v-if="orderItems.length">
        <thead>
          <tr>
            <th>Produit</th>
            <th>Quantité</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in orderItems" :key="item.id">
            <td>{{ item.product }}</td>
            <td>{{ item.quantity }}</td>
          </tr>
        </tbody>
      </table>

      <h3>Paiements</h3>
      <table v-if="payments.length">
        <thead>
          <tr>
            <th>Montant</th>
            <th>Mode</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in payments" :key="p.id">
            <td>{{ p.amount }}</td>
            <td>{{ p.mode }}</td>
            <td>{{ p.description }}</td>
          </tr>
        </tbody>
      </table>

      <h3>Ajouter un paiement</h3>
      <div>
        <input type="number" v-model.number="newPayment.amount" placeholder="Montant"/>
        <input type="text" v-model="newPayment.mode" placeholder="Mode"/>
        <input type="text" v-model="newPayment.description" placeholder="Description"/>
        <button @click="addPayment">Ajouter</button>
      </div>
    </div>

    <h2>Nouvelle commande</h2>
    <div>
      <select v-model="newOrder.partner_id">
        <option v-for="c in partners" :key="c.id" :value="c.id">{{ c.name }}</option>
      </select>
      <h3>Produits</h3>
      <div v-for="(item, index) in newOrderItems" :key="index" class="product-line">
        <select v-model="item.product_id">
          <option v-for="p in products" :key="p.id" :value="p.id">{{ p.name }}</option>
        </select>
        <input type="number" v-model.number="item.quantity" placeholder="Quantité"/>
        <button @click="removeNewItem(index)">Supprimer</button>
      </div>
      <button @click="addNewItemLine">Ajouter produit</button>
      <button @click="createOrder">Créer commande</button>
    </div>
  </div>
</template>

<script>
import api from '../axios';

export default {
  data() {
    return {
      orders: [],
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
  methods: {
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
    async selectOrder(order) {
      this.selectedOrder = order;
      // Récupérer les items
      const resItems = await api.get(`/api/order-items/?order_id=${order.id}`);
      this.orderItems = resItems.data;
      // Récupérer les paiements
      const resPayments = await api.get(`/api/payments/?partner=${order.partner_id}`);
      this.payments = resPayments.data;
    },
    addNewItemLine() {
      this.newOrderItems.push({ product_id: null, quantity: 1 });
    },
    removeNewItem(index) {
      this.newOrderItems.splice(index, 1);
    },
    async createOrder() {
      if (!this.newOrder.partner_id) return;
      const res = await api.post('/api/orders/', {
        partner_id: this.newOrder.partner_id,
        products: this.newOrderItems.map(i => i.product_id)
      });
      this.orders.push(res.data);
      this.newOrder.partner_id = null;
      this.newOrderItems = [];
    },
    async addPayment() {
      if (!this.selectedOrder) return;
      const res = await api.post('/api/payments/', {
        partner_id: this.selectedOrder.partner_id,
        amount: this.newPayment.amount,
        mode: this.newPayment.mode,
        description: this.newPayment.description
      });
      this.payments.push(res.data);
      this.newPayment = { amount: 0, mode: '', description: '' };
    }
  }
}
</script>

<style scoped>
/* Style chocolat */
div { font-family: 'Segoe UI', sans-serif; padding: 20px; background-color: #f5ece3; border-radius: 10px; }
h2,h3 { color: #4b2e2e; }
ul { list-style: none; padding: 0; }
li { padding: 8px 12px; margin-bottom: 5px; border-radius: 6px; cursor: pointer; background-color: #fff8f0; transition: 0.3s; }
li:hover { background-color: #d9b99b; }
.selected { font-weight: bold; background-color: #7b4f4f; color: #fff8f0; }
table { width: 100%; border-collapse: separate; border-spacing: 0; margin-top: 10px; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 8px rgba(75,46,46,0.3); }
thead { background-color: #4b2e2e; color: #fff8f0; }
th, td { padding: 10px 12px; text-align: left; }
tbody tr:nth-child(even) { background-color: #d9b99b; }
tbody tr:hover { background-color: #7b4f4f; color: #fff8f0; }
select, input, button { padding: 6px 10px; margin: 5px 0; border-radius: 6px; border: 1px solid #7b4f4f; }
button { background-color: #7b4f4f; color: #fff8f0; cursor: pointer; border: none; transition: 0.3s; }
button:hover { background-color: #8c5c5c; }
.product-line { display: flex; gap: 5px; align-items: center; margin-bottom: 5px; }
</style>
