<template>
  <div class="partner-list">
    <div class="header">
      <h2>Liste des partenaires</h2>
      <button class="btn-create" @click="goToCreate">➕ Créer un partenaire</button>
    </div>

    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Nom</th>
          <th>Email</th>
          <th>Entreprise</th>
          <th>Numéro</th>
          <th>Rue</th>
          <th>Ville</th>
          <th>Pays</th>
          <th>Type</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="partner in partners" :key="partner.id">
          <td>{{ partner.id }}</td>
          <td>{{ partner.name }}</td>
          <td>{{ partner.email }}</td>
          <td>{{ partner.company ? partner.company.name : '-' }}</td>
          <td>{{ partner.phone || '-' }}</td>
          <td>{{ partner.street || '-' }}</td>
          <td>{{ partner.city || '-' }}</td>
          <td>{{ partner.country || '-' }}</td>
          <td>{{ partner.type || '-' }}</td>
          <td>
            <button class="btn-edit" @click="goToEdit(partner.id)">✏️ Modifier</button>
            <button class="btn-delete" @click="deletePartner(partner.id)">🗑️ Supprimer</button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-if="loading">Chargement...</p>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import api from '../axios';
export default {
  name: 'PartnerList',
  data() {
    return {
      partners: [],
      loading: false,
      error: null,
    };
  },
  created() {
    this.fetchPartners();
  },
  methods: {
    async fetchPartners() {
      this.loading = true;
      try {
        const token = localStorage.getItem('access_token');
        const response = await api.get('http://localhost:8000/api/partners/', {
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
      this.$router.push({ name: 'Partners' }); // la route de création
    },

    goToEdit(id) {
      this.$router.push({ name: 'EditPartner', params: { id } }); // prévoir la route EditPartner
    },

    async deletePartner(id) {
      if (!confirm("Voulez-vous vraiment supprimer ce partenaire ?")) return;
      try {
        const token = localStorage.getItem('access_token');
        await api.delete(`http://localhost:8000/api/partners/${id}/`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.partners = this.partners.filter(p => p.id !== id);
      } catch (err) {
        console.error(err);
        alert("Erreur lors de la suppression.");
      }
    }
  }
};
</script>
<style scoped>
.partner-list {
  margin: 2rem;
  font-family: 'Roboto', sans-serif;
  background: #fff8f0;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.1);
}

/* Titre */
.partner-list h2 {
  color: #4b2e2b;
  font-family: 'Pacifico', cursive;
  margin-bottom: 1.5rem;
  font-size: 2rem;
  text-align: center;
}

/* Bouton créer */
.btn-create {
  background-color: #d2691e; /* caramel */
  color: #fff;
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  margin-bottom: 1rem;
  transition: background 0.3s ease;
}
.btn-create:hover {
  background-color: #8b4513; /* brun chocolat */
}

/* Tableau */
table {
  width: 100%;
  border-collapse: collapse;
  background-color: #fff4e6;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

th, td {
  padding: 12px 15px;
  text-align: left;
}

thead th {
  background-color: #8b4513; /* brun chocolat */
  color: #fff;
  font-weight: 600;
}

tbody tr:nth-child(even) {
  background-color: #ffe6cc; /* beige clair */
}

tbody tr:hover {
  background-color: #f2d1a1; /* caramel clair */
}

/* Boutons Modifier / Supprimer */
.btn-edit, .btn-delete {
  padding: 0.4rem 0.8rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  margin-right: 5px;
  color: #fff;
  font-weight: bold;
  transition: all 0.3s ease;
}

.btn-edit {
  background-color: #c2691e;
}
.btn-edit:hover {
  background-color: #8b4513;
}

.btn-delete {
  background-color: #a52a2a; /* rouge brun */
}
.btn-delete:hover {
  background-color: #7b1f1f;
}

/* Messages chargement / erreur */
p {
  margin-top: 1rem;
  font-weight: bold;
  text-align: center;
}

p[style*="color: red"] {
  color: #a52a2a;
}
</style>

