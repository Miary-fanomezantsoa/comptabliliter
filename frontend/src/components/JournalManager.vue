<template>
  <div class="min-h-screen bg-gradient-to-br from-orange-50 to-orange-100 p-4 font-sans flex flex-col items-center">
    <!-- Header -->
    <div class="w-full max-w-xl bg-orange-600 text-white p-4 rounded-xl shadow-md mb-4 flex justify-between items-center">
      <h1 class="text-2xl font-bold flex items-center gap-2">🧾 Journal Comptable</h1>
    </div>

    <!-- Statistiques rapides -->
    <div v-if="selectedJournal" class="w-full max-w-xl bg-white p-4 rounded-xl shadow-md mb-4 flex justify-between text-sm sm:text-base">
      <div>
        <p class="text-orange-800 font-semibold">Écritures:</p>
        <p class="font-bold">{{ journalEntries.length }}</p>
      </div>
      <div>
        <p class="text-orange-800 font-semibold">Total Débit:</p>
        <p class="font-bold">{{ totalDebit }}</p>
      </div>
      <div>
        <p class="text-orange-800 font-semibold">Total Crédit:</p>
        <p class="font-bold">{{ totalCredit }}</p>
      </div>
    </div>

    <!-- Choix du journal -->
    <div class="w-full max-w-xl bg-white p-4 rounded-xl shadow-md mb-4">
      <h2 class="text-lg font-semibold text-orange-800 mb-2">Choisissez le journal</h2>
      <select v-model="selectedJournal" @change="selectJournal(selectedJournal)"
              class="p-2 w-full rounded border border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-600">
        <option disabled value="">Sélectionnez un journal</option>
        <option v-for="j in journals" :key="j.id" :value="j">{{ j.name }}</option>
      </select>
    </div>

    <!-- Liste des écritures -->
    <div class="w-full max-w-xl bg-white p-4 rounded-xl shadow-md mb-4">
      <h2 class="text-lg font-semibold text-orange-800 mb-2">Écritures</h2>
      <ul>
        <li v-for="e in journalEntries" :key="e.id"
            @click="selectEntry(e)"
            :class="['p-2 mb-1 rounded cursor-pointer transition-transform transform hover:scale-105',
                    selectedEntry && selectedEntry.id === e.id
                      ? 'bg-orange-600 text-white font-bold shadow-md'
                      : 'bg-orange-100 hover:bg-orange-200']">
          {{ e.reference || 'Sans référence' }} - {{ e.date }} | Partenaire:
          <span class="font-medium">{{ e.items[0]?.account?.name || 'Aucun' }}</span>
        </li>
      </ul>
    </div>

    <!-- Table des lignes -->
    <div v-if="journalItems.length" class="w-full max-w-xl bg-white p-4 rounded-xl shadow-md mb-4 overflow-x-auto">
      <h2 class="text-lg font-semibold text-orange-800 mb-2">Lignes de l'écriture</h2>
      <table class="min-w-full border border-orange-300 rounded-lg">
        <thead class="bg-orange-900 text-white">
          <tr>
            <th class="p-2 text-left">Compte</th>
            <th class="p-2 text-right">Débit</th>
            <th class="p-2 text-right">Crédit</th>
            <th class="p-2 text-left">Libellé</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in journalItems" :key="item.id" class="even:bg-orange-50 hover:bg-orange-200 transition-colors">
            <td class="p-2 font-medium">{{ item.account.name }}</td>
            <td class="p-2 text-right font-mono">{{ item.debit || 0 }}</td>
            <td class="p-2 text-right font-mono">{{ item.credit || 0 }}</td>
            <td class="p-2">{{ item.label }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Formulaire d'ajout -->
    <div v-if="selectedEntry" class="w-full max-w-xl bg-white p-4 rounded-xl shadow-md mb-4">
      <h3 class="text-lg font-semibold text-orange-800 mb-2">Ajouter une ligne</h3>
      <select v-model="newItem.account_id"
              class="p-2 mb-2 rounded border border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-600 w-full">
        <option disabled value="">Sélectionnez un compte</option>
        <option v-for="c in accounts" :key="c.id" :value="c.id">{{ c.name }}</option>
      </select>

      <div class="flex flex-col sm:flex-row gap-2 mb-2">
        <input type="number" v-model.number="newItem.debit" placeholder="Débit"
               class="p-2 rounded border border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-600 flex-1"/>
        <input type="number" v-model.number="newItem.credit" placeholder="Crédit"
               class="p-2 rounded border border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-600 flex-1"/>
      </div>

      <input type="text" v-model="newItem.label" placeholder="Libellé"
             class="p-2 mb-2 rounded border border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-600 w-full"/>

      <button @click="addItem"
              class="w-full sm:w-auto px-4 py-2 bg-orange-600 text-white font-bold rounded hover:bg-orange-700 transition-colors">
        ➕ Ajouter
      </button>
    </div>
  </div>
</template>

<script>
import api from '../axios';

export default {
  data() {
    return {
      journals: [],
      selectedJournal: null,
      journalEntries: [],
      selectedEntry: null,
      journalItems: [],
      accounts: [],
      newItem: { account_id: null, debit: null, credit: null, label: '' },
      loading: false
    };
  },
  computed: {
    totalDebit() {
      return this.journalItems.reduce((sum, i) => sum + (i.debit || 0), 0);
    },
    totalCredit() {
      return this.journalItems.reduce((sum, i) => sum + (i.credit || 0), 0);
    }
  },
  created() {
    this.fetchJournals();
    this.fetchAccounts();
  },
  methods: {
    async fetchJournals() {
      this.loading = true;
      try { this.journals = (await api.get('/api/journals/')).data; }
      catch (err) { console.error(err); }
      finally { this.loading = false; }
    },
    async fetchAccounts() {
      try { this.accounts = (await api.get('/api/comptes/')).data; }
      catch (err) { console.error(err); }
    },
    async selectJournal(journal) {
      this.selectedJournal = journal;
      this.selectedEntry = null;
      this.journalItems = [];
      this.loading = true;
      try { this.journalEntries = (await api.get('/api/journal-entries/', { params: { journal: journal.id } })).data; }
      catch (err) { console.error(err); }
      finally { this.loading = false; }
    },
    async selectEntry(entry) {
  this.selectedEntry = entry;
  this.loading = true;
  try {
    const res = await api.get(`/api/journal-entries/${entry.id}/`);
    this.journalItems = res.data.items; // récupère déjà les lignes
  } catch (err) {
    console.error(err);
  } finally {
    this.loading = false;
  }
},

    async addItem() {
      if (!this.selectedEntry || !this.newItem.account_id) return;
      try {
        const res = await api.post('/api/journal-items/', {
          entry_id: this.selectedEntry.id,
          account_id: this.newItem.account_id,
          debit: this.newItem.debit,
          credit: this.newItem.credit,
          label: this.newItem.label
        });
        this.journalItems.push(res.data);
        this.newItem = { account_id: null, debit: 0, credit: 0, label: '' };
      } catch (err) { console.error(err.response?.data); }
    }
  }
};
</script>
