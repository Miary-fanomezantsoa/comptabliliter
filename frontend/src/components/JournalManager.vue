<template>
  <div class="max-w-4xl mx-auto p-6 bg-orange-50 rounded-xl shadow-md font-sans">
    <!-- Header -->
    <h2 class="text-2xl font-bold text-orange-900 mb-4">Choisissez le type de journal</h2>
    <select v-model="selectedJournal" @change="selectJournal(selectedJournal)"
            class="p-2 mb-6 rounded border border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-600">
      <option v-for="j in journals" :key="j.id" :value="j">{{ j.name }}</option>
    </select>

    <h2 class="text-2xl font-bold text-orange-900 mb-4">Écritures du journal</h2>
    <ul>
      <li
        v-for="e in journalEntries"
        :key="e.id"
        @click="selectEntry(e)"
        :class="['p-3 mb-2 rounded cursor-pointer transition-colors',
                selectedEntry && selectedEntry.id === e.id ? 'bg-orange-600 text-white font-bold' : 'bg-orange-100 hover:bg-orange-200']">
        {{ e.reference || 'Sans référence' }} - {{ e.date }} | Partenaire :
        <span>{{ e.items[0]?.account?.name || 'Aucun' }}</span>
      </li>
    </ul>

    <h2 v-if="journalItems.length" class="text-2xl font-bold text-orange-900 mt-6 mb-4">Lignes de l'écriture</h2>
    <div v-if="journalItems.length" class="overflow-x-auto">
      <table class="min-w-full border border-orange-300 rounded-lg overflow-hidden">
        <thead class="bg-orange-900 text-white">
          <tr>
            <th class="p-2 text-left">Compte</th>
            <th class="p-2 text-right">Débit</th>
            <th class="p-2 text-right">Crédit</th>
            <th class="p-2 text-left">Libellé</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in journalItems" :key="item.id" class="even:bg-orange-100 hover:bg-orange-600 hover:text-white transition-colors">
            <td class="p-2">{{ item.account.name }}</td>
            <td class="p-2 text-right">{{ item.debit }}</td>
            <td class="p-2 text-right">{{ item.credit }}</td>
            <td class="p-2">{{ item.label }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Formulaire ajout -->
    <div v-if="selectedEntry" class="mt-6 p-4 bg-orange-100 rounded-lg shadow-inner">
      <h3 class="text-xl font-semibold text-orange-900 mb-3">Ajouter une ligne d'écriture</h3>
      <h5 class="text-orange-800 mb-2">Sélection du partenaire :</h5>

      <select v-model="newItem.account_id"
              class="p-2 mb-3 rounded border border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-600 w-full">
        <option disabled value="">Sélectionnez un compte</option>
        <option v-for="c in accounts" :key="c.id" :value="c.id">{{ c.name }}</option>
      </select>

      <div class="flex flex-col sm:flex-row gap-3 mb-3">
        <input type="number" v-model.number="newItem.debit" placeholder="Débit"
               class="p-2 rounded border border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-600 flex-1"/>
        <input type="number" v-model.number="newItem.credit" placeholder="Crédit"
               class="p-2 rounded border border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-600 flex-1"/>
      </div>

      <input type="text" v-model="newItem.label" placeholder="Libellé"
             class="p-2 mb-3 rounded border border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-600 w-full"/>

      <button @click="addItem"
              class="px-4 py-2 bg-orange-600 text-white font-semibold rounded hover:bg-orange-700 transition-colors">
        Ajouter
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
      try { this.journalItems = (await api.get(`/api/journal-entries/${entry.id}/ecritures/`)).data; }
      catch (err) { console.error(err); }
      finally { this.loading = false; }
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
