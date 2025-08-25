<template>
  <div class="partner-form">
    <h2>Créer un partenaire</h2>

    <form @submit.prevent="createPartner">
      <!-- Infos principales -->
      <div class="form-section">
        <h3>Informations générales</h3>
        <div class="form-grid">
          <div class="form-group">
            <label>Nom :</label>
            <input v-model="partner.name" type="text" required />
          </div>
          <div class="form-group">

            <select v-model="partner.type">
              <option value="person">Personne</option>
              <option value="company">Entreprise</option>
            </select>
            <label>type:</label>
          </div>
        </div>
      </div>

      <!-- Contact -->
      <div class="form-section">
        <h3>Contact</h3>
        <div class="form-grid">
          <div class="form-group">
            <label>Email :</label>
            <input v-model="partner.email" type="email" />
          </div>
          <div class="form-group">
            <label>Téléphone :</label>
            <input v-model="partner.phone" type="text" />
          </div>
          <div class="form-group">
            <label>Mobile :votre numero fix</label>
            <input v-model="partner.mobile" type="text" />
          </div>
        </div>
      </div>

      <!-- Adresse -->
      <div class="form-section">
        <h3>Adresse</h3>
        <div class="form-grid">
          <div class="form-group">
            <label>Rue :</label>
            <input v-model="partner.street" type="text" />
          </div>
          <div class="form-group">
            <label>Ville :ou ce citue votre point de vente</label>
            <input v-model="partner.city" type="text" />
          </div>
          <div class="form-group">
            <label>Pays : ou ce citue votre point de vente</label>
            <input v-model="partner.country" type="text" />
          </div>
        </div>
      </div>

      <!-- Rôle et Entreprise -->
      <div class="form-section">
        <h3>Rôle et Entreprise</h3>
        <div class="form-grid">
          <div class="form-group">

            <select v-model="partner.role">
              <option value="client">Client</option>
              <option value="supplier">Fournisseur</option>
              <option value="both">Client & Fournisseur</option>
            </select>
            <label>Role:</label>
          </div>
          <div  v-if="partner.type === 'company'" class="form-group">

            <select v-model="selectedCompany">
              <option v-for="c in companies" :key="c.id" :value="c.id">
                {{ c.name }}
              </option>
              <option value="new">+ Nouvelle entreprise</option>
            </select>
            <label>entreprise</label>
          </div>
        </div>
      </div>
       <div v-if="selectedCompany === 'new' && partner.type === 'company'" class="form-group">
          <input v-model="newCompanyName" type="text" placeholder=" " />
          <label>Nom de la nouvelle entreprise</label>
        </div>

      <div class="form-actions">
        <button type="button" @click="createPartner('list')">Créer</button>
        <button type="button" @click="createPartner('another')">Créer et créer un autre</button>
      </div>
    </form>
  </div>
</template>

<script>
import api from "../axios.js"; // ton instance axios configurée avec token

export default {
  data() {
    return {
        selectedCompany: null,
        newCompanyName: "",
      partner: {
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
    };
    console.log(error.response.data)
  },

  async created() {
    try {
      const res = await api.get("/api/companies/"); // utiliser api au lieu de axios
      this.companies = res.data;
      if (this.companies.length) {
        this.partner.company = this.companies[0].id;
      }
    } catch (error) {
      console.error("Erreur lors du chargement des companies:", error);
    }
  },
  methods: {
    async createPartner(mode) {
    let companyId = this.selectedCompany;

      // Si nouvelle entreprise, on la crée d'abord
      if (this.selectedCompany === "new" && this.newCompanyName.trim() !== "") {
        try {
          const res = await api.post("/api/companies/", { name: this.newCompanyName });
          companyId = res.data.id;
          this.companies.push(res.data);
        } catch (error) {
          console.error("Erreur création entreprise:", error);
          alert("Impossible de créer la nouvelle entreprise.");
          return;
        }
      }

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
          company: this.partner.type === "person" ? this.partner.company : null,
        });
        alert("Partenaire créé avec succès !");
        if (mode === "list") {
      this.$router.push({ name: "PartnerList" }); // redirection vers la liste
    } else if (mode === "another") {
      // reset formulaire pour créer un autre partenaire
      this.partner = {
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
      };
      this.selectedCompany = null;
      this.newCompanyName = "";
    }
      } catch (error) {
        console.error(error);
        alert("Erreur lors de la création du partenaire.");
      }
    },
  },
};
</script>


<style scoped>
.partner-form
 {
  max-width: 600px;
  margin: 50px auto;
  background-color: #fdf5f0;
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 12px 25px rgba(0,0,0,0.1);
  font-family: 'Roboto', sans-serif;
}

h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #4b2e2b;
}

.card {
  background: #fff;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 12px 25px rgba(0,0,0,0.1);
}

.form-grid {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 1rem;
}

.form-group {
  position: relative;
  flex: 1 1 30%;
  margin-bottom: 1.5rem;
  min-width: 200px;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 12px 10px;
  border-radius: 10px;
  border: 1px solid #ccc;
  background: #fdf5f0;
  font-size: 0.95rem;
  transition: all 0.3s ease;
}

.form-group label {
  position: absolute;
  top: 12px;
  left: 12px;
  color: #999;
  font-size: 0.9rem;
  pointer-events: none;
  transition: all 0.3s ease;
}

.form-group input:focus + label,
.form-group input:not(:placeholder-shown) + label,
.form-group select:focus + label,
.form-group select:not([value=""]) + label {
  top: -10px;
  left: 10px;
  font-size: 0.75rem;
  background: #fff;
  padding: 0 5px;
  color: #6b3e26;
}

button {
  display: block;
  width: 100%;
  padding: 0.9rem;
  margin-top: 1.5rem;
  background: linear-gradient(145deg, #d2691e, #8b4513);
  color: white;
  font-weight: 600;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

button:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}

/* Responsive */
@media (max-width: 640px) {
  .form-grid {
    flex-direction: column;
  }
}
</style>
