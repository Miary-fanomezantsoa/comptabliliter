<template>
  <div class="min-h-screen p-6 bg-gray-50 font-sans">
    <div class="max-w-full mx-auto">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row justify-between items-center mb-6">
        <h2 class="text-3xl font-bold text-orange-900 mb-4 sm:mb-0">Liste des partenaires</h2>
        <button @click="goToCreate"
                class="px-4 py-2 bg-orange-600 text-white font-semibold rounded hover:bg-orange-700 transition">
          ➕ Créer un partenaire
        </button>
      </div>

      <!-- Barre de recherche -->
      <div class="mb-4 flex flex-col sm:flex-row items-center justify-between gap-4">
        <input v-model="searchQuery"
               type="text"
               placeholder="Rechercher un partenaire..."
               class="w-full sm:w-64 p-2 rounded border border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-600"/>
      </div>

      <!-- Tableau -->
      <div class="overflow-x-auto">
        <table class="min-w-full bg-white rounded-lg shadow-lg text-sm sm:text-base">
          <thead class="bg-orange-700 text-white">
            <tr>
              <th class="px-4 py-2 text-left">ID</th>
              <th class="px-4 py-2 text-left">Nom</th>
              <th class="px-4 py-2 text-left">Email</th>
              <th class="px-4 py-2 text-left">Entreprise</th>
              <th class="px-4 py-2 text-left">Numéro</th>
              <th class="px-4 py-2 text-left">Rue</th>
              <th class="px-4 py-2 text-left">Ville</th>
              <th class="px-4 py-2 text-left">Pays</th>
              <th class="px-4 py-2 text-left">Type</th>
              <th class="px-4 py-2 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="partner in filteredPartners" :key="partner.id"
                class="odd:bg-white even:bg-orange-50 hover:bg-orange-100 transition">
              <td class="px-4 py-2">{{ partner.id }}</td>
              <td class="px-4 py-2">{{ partner.name }}</td>
              <td class="px-4 py-2">{{ partner.email || '-' }}</td>
              <td class="px-4 py-2">{{ partner.company ? partner.company.name : '-' }}</td>
              <td class="px-4 py-2">{{ partner.phone || '-' }}</td>
              <td class="px-4 py-2">{{ partner.street || '-' }}</td>
              <td class="px-4 py-2">{{ partner.city || '-' }}</td>
              <td class="px-4 py-2">{{ partner.country || '-' }}</td>
              <td class="px-4 py-2">{{ partner.type || '-' }}</td>
              <td class="px-4 py-2 space-x-2">
                <button @click="goToEdit(partner.id)"
                        class="px-2 py-1 bg-orange-600 text-white rounded hover:bg-orange-700 transition text-sm">
                  ✏️ Modifier
                </button>
                <button @click="deletePartner(partner.id)"
                        class="px-2 py-1 bg-red-600 text-white rounded hover:bg-red-700 transition text-sm">
                  🗑️ Supprimer
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Messages -->
      <p v-if="loading" class="text-center font-semibold text-orange-700 mt-4">Chargement...</p>
      <p v-if="error" class="text-center font-semibold text-red-700 mt-4">{{ error }}</p>
    </div>
  </div>
</template>


<script>
import api from '../axios';

export default {
  name: 'PartnerList',
  data() {
    return {
      partners: [],
      searchQuery: '',
      loading: false,
      error: null,
    };
  },
  computed: {
  filteredPartners() {
    if (!this.searchQuery) return this.partners;

    const q = this.searchQuery.toLowerCase();

    return this.partners.filter(p => {
      const companyName = p.company?.name || '';
      return (
        String(p.id).includes(q) ||
        p.name.toLowerCase().includes(q) ||
        (p.email && p.email.toLowerCase().includes(q)) ||
        companyName.toLowerCase().includes(q)
      );
    });
  }
},


  created() {
    this.fetchPartners();
  },
  methods: {
    async fetchPartners() {
      this.loading = true;
      try {
        const token = localStorage.getItem('access_token');
        const response = await api.get('/api/partners/', {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.partners = response.data;
      } catch (err) {
        console.error(err);
        this.error = 'Impossible de récupérer les partenaires.';
      } finally {
        this.loading = false;
      }
    },

    goToCreate() {
      this.$router.push({ name: 'Partners' });
    },

   goToEdit(id) {
  this.$router.push({ name: 'Partners', params: { partnerId: id } });
},


    async deletePartner(id) {
      if (!confirm('Voulez-vous vraiment supprimer ce partenaire ?')) return;
      try {
        const token = localStorage.getItem('access_token');
        await api.delete(`/api/partners/${id}/`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.partners = this.partners.filter(p => p.id !== id);
      } catch (err) {
        console.error(err);
        alert('Erreur lors de la suppression.');
      }
    },
  },
};
</script>
