<template>
  <div class="container">
    <h2>Comptes comptables</h2>
    <button @click="openModal()" class="btn-add">Ajouter un compte</button>

    <table>
      <thead>
        <tr>
          <th>Code</th>
          <th>Intitulé</th>
          <th>Type</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="compte in comptes" :key="compte.id">
          <td>{{ compte.code }}</td>
          <td>{{ compte.name }}</td>
          <td>{{ compte.account_type }}</td>
          <td>
            <button @click="openModal(compte)">Modifier</button>
            <button @click="openEcritures(compte)">Voir écritures</button>
             <button @click="deleteCompte(compte.id)" class="delete-btn">Supprimer</button>
          </td>
        </tr>
        <tr v-if="comptes.length === 0">
          <td colspan="4">Aucun compte disponible</td>
        </tr>
      </tbody>
    </table>

    <!-- Modal compte -->
    <div v-if="modalVisible" class="modal">
      <div class="modal-content">
        <h3>{{ form.id ? 'Modifier le compte' : 'Ajouter un compte' }}</h3>
        <form @submit.prevent="saveCompte">
  <input v-if="form.id" v-model="form.code" placeholder="Code" readonly />
  <input v-model="form.name" placeholder="Intitulé" required />

  <!-- Type de compte -->
  <label for="account_type">Type de compte :</label>
<select v-model="form.account_type" id="account_type">
  <option value="" disabled hidden>Choisir un type de compte</option>
  <option v-for="(label, key) in accountTypes" :key="key" :value="key">{{ label }}</option>
</select>

  <!-- Devise -->
  <label>Devise a utiliser</label>
  <select v-model="form.currency">

  <option value="" disabled>Choisir une devise</option>
  <option v-for="c in currencies" :key="c.id" :value="c.id">{{ c.name }}</option>
</select>


  <!-- Rapprochement -->
  <label>
  Rapprochable:
    <input type="checkbox" v-model="form.reconcile" />
  </label>
<br>
<!-- Taxes -->
<label for="tax">Taxe :</label>
<select v-model="form.taxes" id="tax" multiple>
  <option v-for="t in taxes" :key="t.id" :value="t.id">{{ t.name }}</option>
</select>

<!-- Tags -->
<label for="tag">Tag :</label>
<select v-model="form.tags" id="tag" multiple>
  <option v-for="tag in tags" :key="tag.id" :value="tag.id">{{ tag.name }}</option>
</select>


<!-- Partenaire -->
<div v-if="requiresPartner(form.account_type)">
  <label for="partner">Partenaire :</label>
  <select v-model="form.partner" id="partner">
    <option value="" disabled  hidden>Choisir un partenaire</option>
    <option v-for="p in partners" :key="p.id" :value="p.id">{{ p.name }}</option>
  </select>
</div>


  <!-- Note -->
  <textarea v-model="form.note" placeholder="Note (facultatif)"></textarea>

  <button type="submit">{{ form.id ? 'Modifier' : 'Ajouter' }}</button>
  <button type="button" @click="closeModal">Annuler</button>
</form>

      </div>
    </div>

    <!-- Modal écritures -->
    <div v-if="ecritureModalVisible" class="modal">
      <div class="modal-content">
        <h3>Écritures du compte {{ compteSelectionne.code }}</h3>
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Libellé</th>
              <th>Débit</th>
              <th>Crédit</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="e in ecritures" :key="e.id">
              <td>{{ new Date(e.date).toLocaleString() }}</td>
              <td>{{ e.libelle }}</td>
              <td>{{ e.debit }}</td>
              <td>{{ e.credit }}</td>
            </tr>
            <tr v-if="ecritures.length === 0">
              <td colspan="4">Aucune écriture</td>
            </tr>
          </tbody>
        </table>
        <button @click="ecritureModalVisible=false">Fermer</button>
      </div>
    </div>
  </div>
</template>
<script>
import api from '../axios.js';

export default {
  data() {
    return {
      comptes: [],
form: {
      id: null,
      code: '',
      name: '',
      account_type: '',
      currency: null,
      reconcile: false,
      note: '',
      taxes: [],
      tags: [],
      partner: null
    },
    currencies: [],  // liste des devises depuis l'API
    taxes: [],       // liste des taxes depuis l'API
    tags: [],        // liste des tags depuis l'API
    partners: [],
    modalVisible: false,
      ecritureModalVisible: false,
      compteSelectionne: {},
      ecritures: [],
      accountTypes: {
        'asset_receivable': 'Actif à recevoir',
        'asset_cash': 'Caisse / Trésorerie',
        'liability_payable': 'Passif à payer',
        'equity': 'Capitaux propres',
        'income': ' Revenus',
        'expense': ' Dépenses'
      }

    }
  },
  methods: {
  requiresPartner(type) {
      // Les types qui nécessitent un partenaire
      return ["asset_receivable", "liability_payable"].includes(type);
    },
  openModal(compte = null) {
    if(compte) this.form = {
      id: compte.id,
      code: compte.code,
      name: compte.name,
      account_type: compte.account_type,
      currency: compte.currency || null,
      reconcile: compte.reconcile || false,
      note: compte.note || '',
      taxes: compte.taxes || [],
      tags: compte.tags || [],
      partner: compte.partner || null
    };
    else this.form = {
      id: null,
      code: '',
      name: '',
      account_type: '',
      currency: null,
      reconcile: false,
      note: '',
      taxes: [],
      tags: [],
      partner: null
    };
    this.modalVisible = true;
  },

  closeModal() {
    this.modalVisible = false;
    this.form = {
      id: null,
      code: '',
      name: '',
      account_type: '',
      currency: null,
      reconcile: false,
      note: '',
      taxes: [],
      tags: [],
      partner: null
    };
  },
async deleteCompte(id) {
  if (!confirm("Voulez-vous vraiment supprimer ce compte ?")) return;

  try {
    await api.delete(`/api/comptes/${id}/`);
    await this.fetchComptes(); // recharge la liste
  } catch (e) {
    console.error("Erreur deleteCompte:", e.response?.data || e);
    alert("Erreur lors de la suppression : " + JSON.stringify(e.response?.data));
  }
},

  async fetchSelects() {
  const token = localStorage.getItem('access_token');
  try {
    const [curr, tax, tag, part] = await Promise.all([
      api.get('/api/currencies/', { headers: { Authorization: `Bearer ${token}` } }),
      api.get('/api/taxes/', { headers: { Authorization: `Bearer ${token}` } }),
      api.get('/api/account-tags/', { headers: { Authorization: `Bearer ${token}` } }),
      api.get('/api/partners/', { headers: { Authorization: `Bearer ${token}` } })
    ]);
    this.currencies = curr.data;
    this.taxes = tax.data;
    this.tags = tag.data;
    this.partners = part.data;
    console.log("Partenaires récupérés :", this.partners);
  } catch (e) {
    console.error("Erreur fetchSelects:", e);
  }
},


    async fetchComptes() {
      try {
        const res = await api.get('/api/comptes/');
        this.comptes = res.data;
      } catch(e) {
        console.error(e);
      }
    },
    async saveCompte() {
  try {
  console.log("Code:", this.form.code, "Name:", this.form.name, "Type:", this.form.account_type);

    // Vérifie que les champs obligatoires sont remplis
    if (!this.form.name || !this.form.account_type) {
      alert("Veuillez remplir tous les champs obligatoires !");
      return;
    }

    // Prépare le payload pour DRF
    const payload = {
      name: this.form.name,
      account_type: this.form.account_type,
      currency: this.form.currency || null,   // déjà un ID
      reconcile: this.form.reconcile,
      note: this.form.note,
      taxes: Array.isArray(this.form.taxes) ? this.form.taxes : [], // tableau d'IDs
      tags: Array.isArray(this.form.tags) ? this.form.tags : [],    // tableau d'IDs
      partner: this.form.partner || null     // déjà un ID
    };

    // POST ou PUT selon si l'objet existe
    if (this.form.id) {
      await api.put(`/api/comptes/${this.form.id}/`, payload);
    } else {
      await api.post('/api/comptes/', payload);
    }

    // Rafraîchit la liste et ferme le modal
    await this.fetchComptes();
    this.closeModal();

  } catch (e) {
    // Affiche l'erreur détaillée du serveur
    console.error("Erreur saveCompte:", e.response?.data || e);
    alert("Erreur lors de l'enregistrement : " + JSON.stringify(e.response?.data));
  }
},


    async openEcritures(compte) {
      this.compteSelectionne = compte;
      try {
        const res = await api.get(`/api/comptes/${compte.id}/ecritures/`);
        this.ecritures = res.data;
        this.ecritureModalVisible = true;
      } catch(e){ console.error(e); }
    }
  },
  mounted() {
    this.fetchComptes();
    this.fetchSelects(); // charge toutes les listes
  }
}
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: #fdf6f0; /* fond crème clair */
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

h2 {
  color: #5a2d0c; /* marron chocolat */
  margin-bottom: 20px;
  text-align: center;
  font-size: 28px;
  font-weight: bold;
}

button {
  cursor: pointer;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 14px;
  transition: all 0.3s ease;
}

.btn-add {
  background: linear-gradient(45deg,#a0522d,#d2691e); /* chocolat caramel */
  color: #fff;
  font-weight: bold;
  margin-bottom: 20px;
}
.btn-add:hover {
  background: linear-gradient(45deg,#d2691e,#a0522d);
}

table {
  width: 100%;
  border-collapse: collapse;
  background: #fff8f0;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 3px 8px rgba(0,0,0,0.1);
}

th, td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #e6d5c2;
}

th {
  background: #d2691e; /* couleur chocolat */
  color: #fff;
  font-weight: bold;
}

tr:hover {
  background: #fce8d8;
}

td.actions button {
  margin: 2px;
  padding: 6px 10px;
  font-size: 13px;
  border-radius: 6px;
  color: #fff;
}

td.actions button:hover {
  opacity: 0.9;
}

button.edit-btn { background: #8b4513; } /* brun foncé */
button.delete-btn { background: #c04000; } /* rouge chocolat */
button.info-btn { background: #d2a679; color: #3c1e0b; } /* caramel clair */
button.success-btn { background: #a0522d; } /* chocolat */
button.cancel-btn { background: #8c7b6b; } /* gris chocolat */

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(90,45,12,0.7); /* overlay marron translucide */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: #fff3e6; /* crème clair */
  padding: 25px;
  border-radius: 12px;
  width: 600px;
  max-width: 90%;
  max-height: 90%;
  overflow-y: auto;
  box-shadow: 0 5px 20px rgba(0,0,0,0.2);
  position: relative;
}

.modal-content h3 {
  margin-top: 0;
  color: #5a2d0c;
  text-align: center;
}

.modal-content input,
.modal-content select {
  width: 100%;
  padding: 8px;
  margin: 10px 0;
  border-radius: 6px;
  border: 1px solid #d4b89c;
  background: #fff8f0;
}

.modal-content input:focus,
.modal-content select:focus {
  outline: none;
  border-color: #a0522d;
  box-shadow: 0 0 5px #d2691e;
}

.modal-content button {
  margin-top: 10px;
  padding: 8px 15px;
  border-radius: 6px;
  border: none;
  color: #fff;
  background: #a0522d;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s;
}

.modal-content button:hover {
  background: #d2691e;
}

.modal-content button[type="button"] {
  background: #8c7b6b;
  margin-left: 10px;
}

.modal-content table {
  width: 100%;
  margin-top: 15px;
  border-collapse: collapse;
}

.modal-content table th,
.modal-content table td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #e6d5c2;
}

.modal-content table th {
  background: #d2691e;
  color: #fff;
}

.modal-content table tr:hover {
  background: #fce8d8;
}
button.delete-btn {
  background: #c04000; /* rouge chocolat */
  color: #fff;
}
button.delete-btn:hover {
  background: #a83200;
}
</style>