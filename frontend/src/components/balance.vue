<template>
  <div class="balance-container">
    <div class="header-banner">
      <span class="header-title">BALANCE</span>
    </div>

    <table class="balance-table">
      <thead>
        <tr>
          <th rowspan="2" class="col-no">N°</th>
          <th rowspan="2" class="col-intitule">Intitulé des comptes</th>
          <th colspan="2" class="col-total">Total</th>
          <th colspan="2" class="col-solde">Solde</th>
        </tr>
        <tr>
          <th class="col-debit">Débit</th>
          <th class="col-credit">Crédit</th>
          <th class="col-debit">Débit</th>
          <th class="col-credit">Crédit</th>
        </tr>
      </thead>
      <tbody>
  <!-- Classes 1 à 5 -->
  <template v-if="balance.balance_by_type['Classes 1 à 5']">
    <tr v-for="acc in balance.balance_by_type['Classes 1 à 5'].accounts" :key="acc.code">
      <td class="col-no">{{ acc.code }}</td>
      <td class="col-intitule">{{ acc.name }}</td>
      <td class="col-debit total-debit">{{ formatAmount(acc.debit_total) }}</td>
      <td class="col-credit total-credit">{{ formatAmount(acc.credit_total) }}</td>
      <td class="col-debit solde-debit">{{ formatAmount(acc.debit_solde) }}</td>
      <td class="col-credit solde-credit">{{ formatAmount(acc.credit_solde) }}</td>
    </tr>
    <!-- Total Classes 1 à 5 -->
    <tr class="total-row">
      <td colspan="2">Total Classes 1 à 5</td>
      <td class="col-debit">{{ formatAmount(balance.balance_by_type['Classes 1 à 5'].total_debit) }}</td>
      <td class="col-credit">{{ formatAmount(balance.balance_by_type['Classes 1 à 5'].total_credit) }}</td>
      <td class="col-debit">{{ formatAmount(balance.balance_by_type['Classes 1 à 5'].total_debit_solde) }}</td>
      <td class="col-credit">{{ formatAmount(balance.balance_by_type['Classes 1 à 5'].total_credit_solde) }}</td>
    </tr>
  </template>

  <!-- Classes 6 et 7 -->
  <template v-if="balance.balance_by_type['Classes 6 et 7']">
    <tr v-for="acc in balance.balance_by_type['Classes 6 et 7'].accounts" :key="acc.code">
      <td class="col-no">{{ acc.code }}</td>
      <td class="col-intitule">{{ acc.name }}</td>
      <td class="col-debit total-debit">{{ formatAmount(acc.debit_total) }}</td>
      <td class="col-credit total-credit">{{ formatAmount(acc.credit_total) }}</td>
      <td class="col-debit solde-debit">{{ formatAmount(acc.debit_solde) }}</td>
      <td class="col-credit solde-credit">{{ formatAmount(acc.credit_solde) }}</td>
    </tr>
    <!-- Total Classes 6 et 7 -->
    <tr class="total-row">
      <td colspan="2">Total Classes 6 et 7</td>
      <td class="col-debit">{{ formatAmount(balance.balance_by_type['Classes 6 et 7'].total_debit) }}</td>
      <td class="col-credit">{{ formatAmount(balance.balance_by_type['Classes 6 et 7'].total_credit) }}</td>
      <td class="col-debit">{{ formatAmount(balance.balance_by_type['Classes 6 et 7'].total_debit_solde) }}</td>
      <td class="col-credit">{{ formatAmount(balance.balance_by_type['Classes 6 et 7'].total_credit_solde) }}</td>
    </tr>
  </template>

  <!-- Totaux généraux -->
  <tr class="grand-total-row">
    <td colspan="2">Totaux généraux</td>
    <td class="col-debit">{{ formatAmount(balance.grand_total_debit_total) }}</td>
    <td class="col-credit">{{ formatAmount(balance.grand_total_credit_total) }}</td>
    <td class="col-debit">{{ formatAmount(balance.grand_total_debit_solde) }}</td>
    <td class="col-credit">{{ formatAmount(balance.grand_total_credit_solde) }}</td>
  </tr>
</tbody>

    </table>

    <p v-if="!balance.is_balanced" class="not-balanced">⚠ La balance n'est pas équilibrée !</p>
  </div>
</template>

<script>
import api from '../axios';

export default {
  data() {
    return {
      balance: {
        balance_by_type: {
          "Classes 1 à 5": {
            accounts: [],
            total_debit: 0,
            total_credit: 0,
            total_debit_solde: 0,
            total_credit_solde: 0
          },
          "Classes 6 et 7": {
            accounts: [],
            total_debit: 0,
            total_credit: 0,
            total_debit_solde: 0,
            total_credit_solde: 0
          }
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
.balance-container {
  font-family: 'Arial', sans-serif;
  max-width: 900px;
  margin: 20px auto;
  border: 1px solid #000;
  box-shadow: 0 0 0 rgba(0, 0, 0, 0); /* Pas d'ombre par défaut pour coller à l'image */
  background-color: #fff; /* Fond blanc */
}

.header-banner {
  background-color: #0c4d0c; /* Vert foncé */
  color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px 15px;
  font-weight: bold;
  font-size: 0.9em;
}

.header-text {
  flex-grow: 1;
  text-align: left;
  white-space: nowrap;
}

.header-title {
  font-size: 1.5em; /* Taille plus grande pour "BALANCE" */
  text-align: right;
  white-space: nowrap;
}

.balance-table {
  width: 100%;
  border-collapse: collapse;
}

.balance-table thead tr:first-child th {
  background-color: #e0e0e0; /* Gris clair pour les en-têtes principaux */
  border: 1px solid #000;
  padding: 8px;
  font-weight: bold;
}

.balance-table thead tr:nth-child(2) th {
  background-color: #e0e0e0; /* Gris clair pour les sous-en-têtes */
  border: 1px solid #000;
  padding: 5px;
  font-weight: bold;
}

.balance-table th, .balance-table td {
  border: 1px solid #000;
  padding: 6px;
  text-align: center;
  font-size: 0.85em;
  color: #000; /* Texte noir par défaut */
}

.col-no {
  width: 5%;
}

.col-intitule {
  width: 30%;
  text-align: left; /* Aligner à gauche pour l'intitulé */
}

.col-total, .col-solde {
  background-color: #e0e0e0; /* Gris clair pour les en-têtes de Total et Solde */
}

/* Couleurs spécifiques pour les colonnes Débit et Crédit comme sur l'image */
.total-debit, .solde-debit {
  background-color: #d9edf7; /* Bleu clair */
}

.total-credit, .solde-credit {
  background-color: #f2dede; /* Rose clair */
}

.total-row {
  font-weight: bold;
  background-color: #e0e0e0; /* Fond gris pour les lignes de totaux */
}

.total-classes1-5 td:first-child,
.total-classes6-7 td:first-child,
.grand-total-row td:first-child {
  background-color: #e0e0e0; /* Gris clair pour la première colonne des totaux */
}

.grand-total-row {
  background-color: #c9c9c9; /* Gris un peu plus foncé pour le total général */
}

.not-balanced {
  color: red;
  font-weight: bold;
  text-align: center;
  margin-top: 10px;
  padding: 10px;
  border-top: 1px solid #000;
  background-color: #fff;
}
</style>