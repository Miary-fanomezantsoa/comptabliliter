<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-4">Grand Livre</h2>

    <!-- Formulaire de filtre période -->
    <div class="mb-4 flex gap-2 items-center">
      <input type="date" v-model="startDate" class="border px-2 py-1 rounded" />
      <input type="date" v-model="endDate" class="border px-2 py-1 rounded" />
      <button
        @click="fetchLedger"
        class="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600"
      >
        Filtrer
      </button>
    </div>

    <!-- Table Grand Livre -->
    <table class="w-full border">
      <thead class="bg-gray-200">
        <tr>
          <th class="p-2 border">Compte</th>
          <th class="p-2 border">Total Débit</th>
          <th class="p-2 border">Total Crédit</th>
          <th class="p-2 border">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(data, account) in ledger" :key="account">
          <td class="p-2 border font-semibold">{{ account }}</td>
          <td class="p-2 border">{{ data.debit }}</td>
          <td class="p-2 border">{{ data.credit }}</td>
          <td class="p-2 border">
            <button
              @click="openModal(account)"
              class="text-blue-500 hover:underline"
            >
              Détails
            </button>
          </td>
        </tr>
      </tbody>
    </table>

   <!-- Modal Détails Grand Livre -->
<div v-if="selectedAccount" class="modal">
  <div class="modal-content">
    <button @click="closeModal" class="close-btn">&times;</button>
    <h3>Détails du compte : {{ selectedAccount }}</h3>

    <table>
      <thead>
        <tr>
          <th>Date</th>
          <th>Journal</th>
          <th>Référence</th>
          <th>Libellé</th>
          <th>Débit</th>
          <th>Crédit</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(entry, i) in ledger[selectedAccount].entries" :key="i">
          <td>{{ entry.date }}</td>
          <td>{{ entry.journal }}</td>
          <td>{{ entry.ref }}</td>
          <td>{{ entry.label }}</td>
          <td>{{ entry.debit }}</td>
          <td>{{ entry.credit }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

  </div>
</template>

<script>
export default {
  name: "GeneralLedger",
  data() {
    return {
      ledger: {},
      startDate: "",
      endDate: "",
      selectedAccount: null,
    };
  },
  methods: {
    async fetchLedger() {
      let url = "/api/general-ledger/";
      const params = [];

      if (this.startDate) params.push(`start_date=${this.startDate}`);
      if (this.endDate) params.push(`end_date=${this.endDate}`);

      if (params.length) url += "?" + params.join("&");

      const res = await fetch(url);
      this.ledger = await res.json();
    },
    openModal(account) {
      this.selectedAccount = account;
    },
    closeModal() {
      this.selectedAccount = null;
    },
  },
  mounted() {
    this.fetchLedger();
  },
};
</script>

<style>
table {
  border-collapse: collapse;
}

/* Animation pour la modal */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
.modal {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: rgba(0,0,0,0.5); /* overlay semi-transparent */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: #fff;
  padding: 25px;
  border-radius: 12px;
  width: 700px;
  max-width: 90%;
  max-height: 90%;
  overflow-y: auto;
  position: relative;
}

.close-btn {
  position: absolute;
  top: 10px; right: 15px;
  font-size: 24px;
  color: #333;
  cursor: pointer;
}

</style>
