<template>
  <div class="balance-container">
    <h2>Balance Comptable</h2>

    <div v-for="(accounts, typeName) in balance.balance_by_type" :key="typeName" class="category-section">
      <h3>{{ typeName }}</h3>
      <table>
        <thead>
          <tr>
            <th>Code</th>
            <th>Nom du Compte</th>
            <th>Débit (Ar)</th>
            <th>Crédit (Ar)</th>
            <th>Solde (Ar)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="acc in accounts" :key="acc.code">
            <td>{{ acc.code }}</td>
            <td>{{ acc.name }}</td>
            <td>{{ formatAmount(acc.debit) }}</td>
            <td>{{ formatAmount(acc.credit) }}</td>
            <td>{{ formatAmount(acc.balance) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h3>Totaux Généraux</h3>
    <p>Débit: {{ formatAmount(balance.grand_total_debit) }} / Crédit: {{ formatAmount(balance.grand_total_credit) }}</p>
    <p v-if="!balance.is_balanced" class="not-balanced">⚠ La balance n'est pas équilibrée !</p>
  </div>
</template>

<script>
import api from '../axios';

export default {
  data() {
    return {
      balance: {
        balance_by_type: {},
        grand_total_debit: 0,
        grand_total_credit: 0,
        is_balanced: true
      }
    };
  },
  async created() {
    try {
      const res = await api.get('/api/trial-balance-by-type/');
      this.balance = res.data;
    } catch (err) {
      console.error("Erreur récupération balance :", err);
    }
  },
  methods: {
    formatAmount(value) {
      return Number(value).toLocaleString('fr-FR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    }
  }
};
</script>

<style scoped>
.balance-container {
  font-family: 'Segoe UI', sans-serif;
  max-width: 1000px;
  margin: 20px auto;
  padding: 20px;
  background-color: #f5ece3;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(75,46,46,0.2);
}

h2 {
  text-align: center;
  color: #4b2e2e;
  font-size: 2em;
  margin-bottom: 20px;
}

h3 {
  color: #4b2e2e;
  margin-top: 20px;
  margin-bottom: 10px;
}

table {
  width: 100%;
  border-collapse: collapse;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(75,46,46,0.15);
  margin-bottom: 10px;
}

thead {
  background-color: #4b2e2e;
  color: #fff8f0;
}

th, td {
  padding: 10px;
  text-align: center;
}

tbody tr:nth-child(even) {
  background-color: #d9b99b;
}

tbody tr:hover {
  background-color: #7b4f4f;
  color: #fff8f0;
  transition: 0.3s;
}

.not-balanced {
  color: red;
  font-weight: bold;
  text-align: center;
  margin-top: 10px;
}

/* Responsive */
@media (max-width: 768px) {
  .balance-container { padding: 15px; margin: 10px; }
  table { font-size: 0.9em; }
  h2 { font-size: 1.6em; }
  h3 { font-size: 1.3em; }
}

@media (max-width: 480px) {
  table { font-size: 0.8em; }
  h2 { font-size: 1.4em; }
  h3 { font-size: 1.1em; }
}
</style>
