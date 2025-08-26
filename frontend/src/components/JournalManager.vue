<template>
  <div class="journal-container">
    <h2>Choisissez le type de journal</h2>
    <select v-model="selectedJournal" @change="selectJournal(selectedJournal)">
      <option v-for="j in journals" :key="j.id" :value="j">{{ j.name }}</option>
    </select>

    <h2>Écritures du journal</h2>
    <ul>
      <li
        v-for="e in journalEntries"
        :key="e.id"
        @click="selectEntry(e)"
        :class="{ selected: selectedEntry && selectedEntry.id === e.id }"
      >
        {{ e.reference || 'Sans référence' }} - {{ e.date }}
        |Partenaire :
    <span>

      {{ e.items[0].account.name || 'Aucun' }}
    </span>
      </li>
    </ul>

   <h2 v-if="journalItems.length">Lignes de l'écriture</h2>
    <table v-if="journalItems.length">

      <thead>
        <tr>
          <th>Compte</th>
          <th>Débit</th>
          <th>Crédit</th>
          <th>Libellé</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in journalItems" :key="item.id">
          <td>{{ item.account.name }}</td>
          <td>{{ item.debit }}</td>
          <td>{{ item.credit }}</td>
          <td>{{ item.label }}</td>
        </tr>
      </tbody>
    </table>


    <div v-if="selectedEntry" class="add-item-form">
    <h3>Ajouter une ligne d'ecriture</h3>
    <h5>Séléction du partenaire:</h5>
      <select v-model="newItem.account_id">
      <option disabled value="">Sélectionnez un compte</option>
        <option v-for="c in accounts" :key="c.id" :value="c.id">{{ c.name }}</option>
      </select>

      <input type="number" v-model.number="newItem.debit" placeholder="Débit" />
      <input type="number" v-model.number="newItem.credit" placeholder="Crédit" />
      <input type="text" v-model="newItem.label" placeholder="Libellé" />
      <button @click="addItem">Ajouter</button>
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
      newItem: {
        account_id: null,
        debit: null,
        credit: null,
        label: ''
      },
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
      try {
        const res = await api.get('/api/journals/');
        this.journals = res.data;
      } catch (err) {
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
    async fetchAccounts() {
      try {
        const res = await api.get('/api/comptes/');
        this.accounts = res.data;
      } catch (err) {
        console.error(err);
      }
    },
    async selectJournal(journal) {
      this.selectedJournal = journal;
      this.selectedEntry = null;
      this.journalItems = [];
      this.loading = true;
      try {
        const res = await api.get('/api/journal-entries/', { params: { journal: journal.id } });
        this.journalEntries = res.data;
      } catch (err) {
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
    async selectEntry(entry) {
      this.selectedEntry = entry;
      this.loading = true;
      try {
        const res = await api.get(`/api/journal-entries/${entry.id}/ecritures/`);
        this.journalItems = res.data;
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
        // reset
        this.newItem = { account_id: null, debit: 0, credit: 0, label: '' };
      } catch (err) {
        console.error(err.response.data);
      }
    }
  }
};
</script>

<style>
/* Variables chocolat globales */
:root {
  --choco-dark: #4b2e2e;
  --choco-medium: #7b4f4f;
  --choco-light: #d9b99b;
  --choco-hover: #8c5c5c;
  --choco-bg: #f5ece3;
  --choco-white: #fff8f0;
}

.journal-container {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: var(--choco-bg);
  padding: 25px;
  border-radius: 12px;
  max-width: 900px;
  margin: 20px auto;
}

h2, h3 {
  color: var(--choco-dark);
  margin-bottom: 12px;
  font-weight: 600;
}

select, input, button {
  padding: 8px 12px;
  margin: 5px 5px 10px 0;
  border-radius: 6px;
  border: 1px solid var(--choco-medium);
  font-size: 14px;
}

select:focus, input:focus {
  outline: none;
  border-color: var(--choco-dark);
  box-shadow: 0 0 5px rgba(75, 46, 46, 0.5);
}

button {
  background-color: var(--choco-medium);
  color: var(--choco-white);
  cursor: pointer;
  transition: 0.3s;
  border: none;
}

button:hover {
  background-color: var(--choco-hover);
}

ul {
  list-style-type: none;
  padding: 0;
  margin-bottom: 20px;
}

li {
  padding: 10px 14px;
  margin-bottom: 6px;
  border-radius: 6px;
  cursor: pointer;
  background-color: var(--choco-white);
  transition: 0.3s;
}

li:hover {
  background-color: var(--choco-light);
}

.selected {
  font-weight: bold;
  background-color: var(--choco-medium);
  color: var(--choco-white);
}

table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin-top: 15px;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 3px 10px rgba(75, 46, 46, 0.3);
}

thead {
  background-color: var(--choco-dark);
  color: var(--choco-white);
}

th, td {
  padding: 10px 12px;
  text-align: left;
}

tbody tr:nth-child(even) {
  background-color: var(--choco-light);
}

tbody tr:hover {
  background-color: var(--choco-medium);
  color: var(--choco-white);
}

.add-item-form {
  margin-top: 15px;
}
</style>
