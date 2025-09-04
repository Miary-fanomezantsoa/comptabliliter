<template>
  <div class="max-w-2xl mx-auto p-6 bg-orange-50 rounded-xl shadow-md font-sans">
    <h2 class="text-2xl font-bold text-orange-900 text-center mb-6">
      {{ isEdit ? "Modifier le partenaire" : "Créer un partenaire" }}
    </h2>

    <form @submit.prevent="isEdit ? updatePartner() : createPartner('list')">

      <!-- Informations générales -->
      <div class="mb-6">
        <h3 class="text-xl font-semibold text-orange-800 mb-3">Informations générales</h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-orange-700 mb-1">Nom :</label>
            <input v-model="partner.name" type="text" required
                   class="w-full p-2 rounded border border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-600"/>
          </div>
          <div>
            <label class="block text-orange-700 mb-1">Type :</label>
            <select v-model="partner.type"
                    class="w-full p-2 rounded border border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-600">
              <option value="person">Personne</option>
              <option value="company">Entreprise</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Contact -->
      <div class="mb-6">
        <h3 class="text-xl font-semibold text-orange-800 mb-3">Contact</h3>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div>
            <label class="block text-orange-700 mb-1">Email :</label>
            <input v-model="partner.email" type="email"
                   class="w-full p-2 rounded border border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-600"/>
          </div>
          <div>
            <label class="block text-orange-700 mb-1">Téléphone :</label>
            <input v-model="partner.phone" type="text"
                   class="w-full p-2 rounded border border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-600"/>
          </div>
          <div>
            <label class="block text-orange-700 mb-1">Mobile :</label>
            <input v-model="partner.mobile" type="text"
                   class="w-full p-2 rounded border border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-600"/>
          </div>
        </div>
      </div>

      <!-- Adresse -->
      <div class="mb-6">
        <h3 class="text-xl font-semibold text-orange-800 mb-3">Adresse</h3>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div>
            <label class="block text-orange-700 mb-1">Rue :</label>
            <input v-model="partner.street" type="text"
                   class="w-full p-2 rounded border border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-600"/>
          </div>
          <div>
            <label class="block text-orange-700 mb-1">Ville :</label>
            <input v-model="partner.city" type="text"
                   class="w-full p-2 rounded border border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-600"/>
          </div>
          <div>
            <label class="block text-orange-700 mb-1">Pays :</label>
            <input v-model="partner.country" type="text"
                   class="w-full p-2 rounded border border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-600"/>
          </div>
        </div>
      </div>

      <!-- Rôle et Entreprise -->
      <div class="mb-6">
        <h3 class="text-xl font-semibold text-orange-800 mb-3">Rôle et Entreprise</h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-orange-700 mb-1">Rôle :</label>
            <select v-model="partner.role"
                    class="w-full p-2 rounded border border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-600">
              <option value="client">Client</option>
              <option value="supplier">Fournisseur</option>
              <option value="both">Client & Fournisseur</option>
            </select>
          </div>
          <div v-if="partner.type === 'company'">
            <label class="block text-orange-700 mb-1">Entreprise :</label>
            <select v-model="selectedCompany"
                    class="w-full p-2 rounded border border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-600">
              <option v-for="c in companies" :key="c.id" :value="c.id">{{ c.name }}</option>
              <option value="new">+ Nouvelle entreprise</option>
            </select>
          </div>
        </div>
      </div>

      <div v-if="selectedCompany === 'new' && partner.type === 'company'" class="mb-6">
        <label class="block text-orange-700 mb-1">Nom de la nouvelle entreprise :</label>
        <input v-model="newCompanyName" type="text"
               class="w-full p-2 rounded border border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-600"/>
               <label class="block text-orange-700 mb-1 mt-3">Devise :</label>
  <select v-model="newCompanyCurrency" required
          class="w-full p-2 rounded border border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-600">
    <option value="">-- Sélectionnez une devise --</option>
    <option v-for="cur in currencies" :key="cur.id" :value="cur.id">
      {{ cur.code }} - {{ cur.name }}
    </option>
  </select>
      </div>

      <!-- Boutons dynamiques -->
      <div class="flex flex-col sm:flex-row gap-4">
        <button v-if="!isEdit" type="button" @click="createPartner('list')"
                class="w-full sm:w-auto px-4 py-2 bg-orange-600 text-white font-semibold rounded hover:bg-orange-700 transition">
          Créer
        </button>
        <button v-if="!isEdit" type="button" @click="createPartner('another')"
                class="w-full sm:w-auto px-4 py-2 bg-orange-600 text-white font-semibold rounded hover:bg-orange-700 transition">
          Créer et créer un autre
        </button>

        <button v-if="isEdit" type="button" @click="updatePartner"
                class="w-full sm:w-auto px-4 py-2 bg-orange-600 text-white font-semibold rounded hover:bg-orange-700 transition">
          Enregistrer les modifications
        </button>
        <button type="button" @click="$router.push({ name: 'PartnerList' })"
          class="w-full sm:w-auto px-4 py-2 bg-gray-400 text-white font-semibold rounded hover:bg-gray-500 transition">
    Annuler
  </button>
      </div>
    </form>
  </div>
</template>

<script>
import api from "../axios.js";

export default {
  data() {
    return {
      isEdit: false,
      selectedCompany: null,
      newCompanyName: "",
      newCompanyCurrency: "",
      partner: {
        id: null,
        name: "",
        type: "person",
        email: "",
        phone: "",
        mobile: "",
        street: "",
        city: "",
        country: "",
        role: "client",
        company: null,
      },
      companies: [],
      currencies: [],
    };
  },
  async created() {
    try {
      const res = await api.get("/api/companies/");
      this.companies = res.data;

      const curRes = await api.get("/api/currencies/");
      this.currencies = curRes.data;

      const partnerId = this.$route.params.partnerId;
      if (partnerId) {
        const partnerRes = await api.get(`/api/partners/${partnerId}/`);
        this.partner = partnerRes.data;
        this.isEdit = true;
        this.selectedCompany = this.partner.company || null;
      } else if (this.companies.length) {
        this.partner.company = this.companies[0].id;
      }
    } catch (error) {
      console.error(error);
    }
  },

  methods: {
    async createPartner(mode) {
      let companyId = this.selectedCompany;

      if (this.selectedCompany === "new") {
        if (!this.newCompanyName.trim() || !this.newCompanyCurrency) {
          alert("Veuillez entrer un nom d'entreprise et sélectionner une devise.");
          return;
        }

        try {
          const res = await api.post("/api/companies/", {
            name: this.newCompanyName,
            currency: this.newCompanyCurrency,
          });
          companyId = res.data.id;
          this.companies.push(res.data);
        } catch (error) {
          console.error("Erreur création entreprise:", error);
          alert("Impossible de créer la nouvelle entreprise.");
          return;
        }
      }

      // Création du partenaire
      try {
        await api.post("/api/partners/", {
          name: this.partner.name,
          type: this.partner.type,
          email: this.partner.email,
          phone: this.partner.phone,
          mobile: this.partner.mobile,
          street: this.partner.street,
          city: this.partner.city,
          country: this.partner.country,
          is_client: this.partner.role === "client" || this.partner.role === "both",
          is_supplier: this.partner.role === "supplier" || this.partner.role === "both",
          company: this.partner.type === "person" ? this.partner.company : companyId,
        });
        alert("Partenaire créé avec succès !");
        if (mode === "list") this.$router.push({ name: "PartnerList" });
        else if (mode === "another") {
          this.partner = { id:null, name:"", type:"person", email:"", phone:"", mobile:"", street:"", city:"", country:"", role:"client", company:null };
          this.selectedCompany = null;
          this.newCompanyName = "";
          this.newCompanyCurrency = "";
        }
      } catch (error) {
        console.error(error);
        alert("Erreur lors de la création du partenaire.");
      }
    },
    async updatePartner() {
      try {
        await api.put(`/api/partners/${this.partner.id}/`, {
          name: this.partner.name,
          type: this.partner.type,
          email: this.partner.email,
          phone: this.partner.phone,
          mobile: this.partner.mobile,
          street: this.partner.street,
          city: this.partner.city,
          country: this.partner.country,
          is_client: this.partner.role === "client" || this.partner.role === "both",
          is_supplier: this.partner.role === "supplier" || this.partner.role === "both",
          company: this.partner.type === "person" ? this.partner.company : this.selectedCompany,
        });
        alert("Partenaire mis à jour !");
        this.$router.push({ name: "PartnerList" });
      } catch (error) {
        console.error(error);
        alert("Erreur lors de la mise à jour du partenaire.");
      }
    }
  }
};
</script>
