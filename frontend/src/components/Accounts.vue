<template>
  <div>
    <h1>Liste des Comptes</h1>
    <table border="1" cellpadding="8" cellspacing="0">
      <thead>
        <tr>
          <th>Nom</th>
          <th>Code</th>
          <th>Type de compte</th>
          <th>Réconciliation</th>
          <th>Note</th>
          <th>Monnaie</th>
          <th>Taxes</th>
          <th>Étiquettes</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="account in accounts" :key="account.id">
          <td>{{ account.name }}</td>
          <td>{{ account.code }}</td>
          <td>{{ account.account_type }}</td>
          <td>{{ account.reconcile ? 'Oui' : 'Non' }}</td>
          <td>{{ account.note || '-' }}</td>
          <td>{{ account.currency?.name || '-' }}</td>
          <td>
            <ul v-if="account.taxes.length">
              <li v-for="tax in account.taxes" :key="tax.id">{{ tax.name }} ({{ tax.rate }}%)</li>
            </ul>
            <span v-else>-</span>
          </td>
          <td>
            <ul v-if="account.tags.length">
              <li v-for="tag in account.tags" :key="tag.id">{{ tag.name }}</li>
            </ul>
            <span v-else>-</span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const accounts = ref([])

onMounted(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/plancomptable/api/accounts/')
    accounts.value = response.data
  } catch (error) {
    console.error('Erreur lors de la récupération des comptes:', error)
  }
})
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}
th {
  background-color: #f0f0f0;
}
td, th {
  padding: 8px;
  text-align: left;
}
</style>
