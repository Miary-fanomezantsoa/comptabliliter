<template>
  <div class="max-w-5xl mx-auto p-6 bg-gray-50 rounded-xl shadow-md font-sans">
    <!-- Header -->
      <div class="bg-gray-100 text-gray-900 flex justify-between items-center p-6 rounded-t-xl shadow">
      <span class="text-3xl font-bold">BALANCE</span>
    </div>

    <!-- Table -->
    <div class="overflow-x-auto mt-4">
      <table class="min-w-full border border-gray-300 rounded-lg overflow-hidden">
        <thead>
          <tr class="bg-gray-200">
            <th rowspan="2" class="p-3 border-b text-black border-gray-300">N°</th>
            <th rowspan="2" class="p-3 border-b text-black border-gray-300 text-left">Intitulé des comptes</th>
            <th colspan="2" class="p-3 border-b text-black border-gray-300">Total</th>
            <th colspan="2" class="p-3 border-b text-black border-gray-300">Solde</th>
          </tr>
          <tr class="bg-gray-200">
            <th class="p-3 border-b text-black  border-gray-300">Débit</th>
            <th class="p-3 border-b text-black border-gray-300">Crédit</th>
            <th class="p-3 border-b text-black border-gray-300">Débit</th>
            <th class="p-3 border-b text-black border-gray-300">Crédit</th>
          </tr>
        </thead>
        <tbody>
          <!-- Classes 1 à 5 -->
          <template v-if="balance.balance_by_type['Classes 1 à 5']">
            <tr v-for="acc in balance.balance_by_type['Classes 1 à 5'].accounts" :key="acc.code"
                class="hover:bg-gray-100 transition-colors">
              <td class="p-3 text-center text-gray-900">{{ acc.code }}</td>
              <td class="p-3 text-gray-900">{{ acc.name }}</td>
              <td class="p-3 text-right bg-blue-50 text-gray-900">{{ formatAmount(acc.debit_total) }}</td>
              <td class="p-3 text-right bg-red-50 text-gray-900">{{ formatAmount(acc.credit_total) }}</td>
              <td class="p-3 text-right bg-blue-50 text-gray-900">{{ formatAmount(acc.debit_solde) }}</td>
              <td class="p-3 text-right bg-red-50 text-gray-900">{{ formatAmount(acc.credit_solde) }}</td>
            </tr>
            <tr class="font-bold bg-gray-100 text-gray-900">
              <td colspan="2" class="p-3">Total Classes 1 à 5</td>
              <td class="p-3 text-right bg-blue-100">{{ formatAmount(balance.balance_by_type['Classes 1 à 5'].total_debit) }}</td>
              <td class="p-3 text-right bg-red-100">{{ formatAmount(balance.balance_by_type['Classes 1 à 5'].total_credit) }}</td>
              <td class="p-3 text-right bg-blue-100">{{ formatAmount(balance.balance_by_type['Classes 1 à 5'].total_debit_solde) }}</td>
              <td class="p-3 text-right bg-red-100">{{ formatAmount(balance.balance_by_type['Classes 1 à 5'].total_credit_solde) }}</td>
            </tr>
          </template>

          <!-- Classes 6 et 7 -->
          <template v-if="balance.balance_by_type['Classes 6 et 7']">
            <tr v-for="acc in balance.balance_by_type['Classes 6 et 7'].accounts" :key="acc.code"
                class="hover:bg-gray-100 transition-colors">
              <td class="p-3 text-center text-gray-900">{{ acc.code }}</td>
              <td class="p-3 text-gray-900">{{ acc.name }}</td>
              <td class="p-3 text-right bg-blue-50 text-gray-900">{{ formatAmount(acc.debit_total) }}</td>
              <td class="p-3 text-right bg-red-50 text-gray-900">{{ formatAmount(acc.credit_total) }}</td>
              <td class="p-3 text-right bg-blue-50 text-gray-900">{{ formatAmount(acc.debit_solde) }}</td>
              <td class="p-3 text-right bg-red-50 text-gray-900">{{ formatAmount(acc.credit_solde) }}</td>
            </tr>
            <tr class="font-bold bg-gray-100 text-gray-900">
              <td colspan="2" class="p-3">Total Classes 6 et 7</td>
              <td class="p-3 text-right bg-blue-100">{{ formatAmount(balance.balance_by_type['Classes 6 et 7'].total_debit) }}</td>
              <td class="p-3 text-right bg-red-100">{{ formatAmount(balance.balance_by_type['Classes 6 et 7'].total_credit) }}</td>
              <td class="p-3 text-right bg-blue-100">{{ formatAmount(balance.balance_by_type['Classes 6 et 7'].total_debit_solde) }}</td>
              <td class="p-3 text-right bg-red-100">{{ formatAmount(balance.balance_by_type['Classes 6 et 7'].total_credit_solde) }}</td>
            </tr>
          </template>

          <!-- Totaux généraux -->
          <tr class="font-bold bg-gray-200 text-gray-900">
            <td colspan="2" class="p-3">Totaux généraux</td>
            <td class="p-3 text-right bg-blue-200">{{ formatAmount(balance.grand_total_debit_total) }}</td>
            <td class="p-3 text-right bg-red-200">{{ formatAmount(balance.grand_total_credit_total) }}</td>
            <td class="p-3 text-right bg-blue-200">{{ formatAmount(balance.grand_total_debit_solde) }}</td>
            <td class="p-3 text-right bg-red-200">{{ formatAmount(balance.grand_total_credit_solde) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Message si pas équilibré -->
    <p v-if="!balance.is_balanced" class="text-red-700 font-bold text-center mt-4 p-2 border border-red-300 rounded bg-red-100">
      La balance n'est pas équilibrée, veillez vérifier vox notification pour plus de détaille!
    </p>
  </div>
</template>


<script>
import api from '../axios';

export default {
  data() {
    return {
      balance: {
        balance_by_type: {
          "Classes 1 à 5": { accounts: [], total_debit: 0, total_credit: 0, total_debit_solde: 0, total_credit_solde: 0 },
          "Classes 6 et 7": { accounts: [], total_debit: 0, total_credit: 0, total_debit_solde: 0, total_credit_solde: 0 }
        },
        grand_total_debit_total: 0,
        grand_total_credit_total: 0,
        grand_total_debit_solde: 0,
        grand_total_credit_solde: 0,
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
      return Number(value || 0).toLocaleString('fr-FR', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      });
    }
  }
};
</script>

<style scoped>
table th, table td {
  border: 1px solid #d1d5db;
}
</style>