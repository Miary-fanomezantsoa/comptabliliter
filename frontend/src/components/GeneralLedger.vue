<template>
  <div class="min-h-screen p-6 bg-gray-50 font-sans">
    <h2 class="text-3xl font-bold text-gray-800 mb-6 text-center">Grand Livre</h2>

    <!-- Filtre période -->
    <div class="flex flex-col sm:flex-row gap-3 mb-6 justify-center items-center">
      <input type="date" v-model="startDate"
             class="border border-gray-300 rounded px-3 py-2 focus:ring-2 focus:ring-blue-400" />
      <input type="date" v-model="endDate"
             class="border border-gray-300 rounded px-3 py-2 focus:ring-2 focus:ring-blue-400" />
      <button @click="fetchLedger"
              class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition">
        Filtrer
      </button>
    </div>

    <!-- Grand Livre -->
    <div class="overflow-x-auto">
      <table class="min-w-full bg-white shadow-md rounded-lg overflow-hidden">
        <thead class="bg-gray-800 text-white">
          <tr>
            <th class="px-4 py-2 text-left">Compte</th>
            <th class="px-4 py-2 text-left">Date</th>
            <th class="px-4 py-2 text-left">Journal</th>
            <th class="px-4 py-2 text-left">Référence</th>
            <th class="px-4 py-2 text-left">Libellé</th>
            <th class="px-4 py-2 text-left">Débit</th>
            <th class="px-4 py-2 text-left">Crédit</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="(data, account) in ledger" :key="account">
            <tr class="bg-gray-100 font-semibold">
              <td class="px-4 py-2" colspan="7">{{ account }} - Total Débit: {{ data.debit }} | Total Crédit: {{ data.credit }}</td>
            </tr>
            <tr v-for="(entry, i) in data.entries" :key="i" class="hover:bg-gray-50">
              <td class="px-4 py-2"></td>
              <td class="px-4 py-2">{{ entry.date }}</td>
              <td class="px-4 py-2">{{ entry.journal }}</td>
              <td class="px-4 py-2">{{ entry.ref }}</td>
              <td class="px-4 py-2">{{ entry.label }}</td>
              <td class="px-4 py-2">{{ entry.debit }}</td>
              <td class="px-4 py-2">{{ entry.credit }}</td>
            </tr>
          </template>
        </tbody>
      </table>
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
  },
  mounted() {
    this.fetchLedger();
  },
};
</script>

<style scoped>
/* Scroll horizontal pour grandes tables */
table {
  border-collapse: collapse;
}
</style>
