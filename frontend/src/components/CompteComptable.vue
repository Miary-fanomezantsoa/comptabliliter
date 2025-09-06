<template>
  <div class="min-h-screen bg-[#fdf6f0] p-6 font-sans">
    <div class="max-w-7xl mx-auto">
      <!-- Titre -->
      <h2 class="text-3xl sm:text-4xl font-extrabold text-[#5a2d0c] text-center mb-8 flex items-center justify-center gap-2">
        <Package class="w-10 h-10 text-[#5a2d0c]" /> Comptes comptables
      </h2>

      <!-- Bouton ajouter -->
      <div class="flex justify-end mb-4">
        <button @click="openModal()"
          class="flex items-center gap-2 bg-gradient-to-r from-[#a0522d] to-[#d2691e] text-white font-bold px-6 py-3 rounded-xl shadow-lg hover:scale-105 hover:shadow-2xl transition-transform">
          <PlusCircle class="w-5 h-5" /> Ajouter un compte
        </button>
      </div>

      <!-- Search -->
      <div class="mb-4">
        <div class="relative">
          <input
            v-model="searchTerm"
            type="text"
            placeholder="Rechercher un compte..."
            class="w-full sm:w-1/2 p-2 pl-10 border rounded focus:outline-none focus:ring-2 focus:ring-[#d2691e]"
          />
          <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
        </div>
      </div>

      <!-- Tableau -->
      <div class="overflow-x-auto">
        <table class="min-w-full bg-white rounded-xl shadow-lg overflow-hidden">
          <thead class="bg-[#8b4513] text-white">
            <tr>
              <th class="py-3 px-6 text-left">Code</th>
              <th class="py-3 px-6 text-left">Intitulé</th>
              <th class="py-3 px-6 text-left">Type</th>
              <th class="py-3 px-6 text-left">Structure</th>
              <th class="py-3 px-6 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="compte in filteredComptes" :key="compte.id" class="hover:bg-[#fce8d8] transition-colors">
              <td class="py-3 px-6">{{ compte.code }}</td>
              <td class="py-3 px-6">{{ compte.name }}</td>
              <td class="py-3 px-6">{{ compte.account_type }}</td>
              <td class="py-3 px-6">
                {{ compte.classe || '-' }} · {{ compte.sous_classe || '-' }} · {{ compte.compte || '-' }} · {{ compte.sous_compte || '-' }}
              </td>
              <td class="py-3 px-6 flex gap-2 flex-wrap">
                <button @click="openModal(compte)" class="flex items-center gap-1 bg-[#8b4513] text-white px-3 py-1 rounded hover:bg-[#a0522d] transition-colors">
                  <Edit3 class="w-4 h-4" /> Modifier
                </button>
                <button @click="openEcritures(compte)" class="flex items-center gap-1 bg-[#d2a679] text-[#3c1e0b] px-3 py-1 rounded hover:bg-[#e0b58a] transition-colors">
                  <BookOpen class="w-4 h-4" /> Écritures
                </button>
                <button @click="deleteCompte(compte.id)" class="flex items-center gap-1 bg-[#c04000] text-white px-3 py-1 rounded hover:bg-[#a83200] transition-colors">
                  <Trash2 class="w-4 h-4" /> Supprimer
                </button>
              </td>
            </tr>
            <tr v-if="comptes.length === 0">
              <td colspan="5" class="py-4 text-center text-gray-500">Aucun compte disponible</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Modal compte -->
      <transition name="fade">
        <div v-if="modalVisible" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div class="bg-[#fff3e6] rounded-2xl w-full max-w-2xl p-6 shadow-2xl overflow-y-auto max-h-[90vh] relative">
            <button @click="closeModal" class="absolute top-4 right-4 p-1 rounded hover:bg-gray-200">
              <X class="w-5 h-5" />
            </button>

            <h3 class="text-2xl font-bold text-[#5a2d0c] text-center mb-4">
              {{ form.id ? 'Modifier le compte' : 'Ajouter un compte' }}
            </h3>

            <form @submit.prevent="saveCompte" class="space-y-4">
              <input v-if="form.id" v-model="form.code" placeholder="Code" readonly
                class="w-full p-2 rounded border border-[#d4b89c] bg-[#fff8f0] focus:outline-none focus:ring-2 focus:ring-[#d2691e]" />
              <input v-model="form.name" placeholder="Intitulé" required
                class="w-full p-2 rounded border border-[#d4b89c] bg-[#fff8f0] focus:outline-none focus:ring-2 focus:ring-[#d2691e]" />

              <label class="block font-semibold text-[#5a2d0c]">Type de compte :</label>
              <select v-model="form.account_type" class="w-full p-2 rounded border border-[#d4b89c] bg-[#fff8f0] focus:outline-none focus:ring-2 focus:ring-[#d2691e]">
                <option value="" disabled hidden>Choisir un type de compte</option>
                <option v-for="(label, key) in accountTypes" :key="key" :value="key">{{ label }}</option>
              </select>

              <label class="block font-semibold text-[#5a2d0c]">Devise :</label>
              <select v-model="form.currency" class="w-full p-2 rounded border border-[#d4b89c] bg-[#fff8f0] focus:outline-none focus:ring-2 focus:ring-[#d2691e]">
                <option value="" disabled>Choisir une devise</option>
                <option v-for="c in currencies" :key="c.id" :value="c.id">{{ c.name }}</option>
              </select>

              <!-- Classe / sous-classe / compte / sous-compte -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label class="block font-semibold text-[#5a2d0c]">Classe :</label>
                  <select v-model="form.classe" @change="onClasseChange"
                    class="w-full p-2 rounded border border-[#d4b89c] bg-[#fff8f0] focus:outline-none focus:ring-2 focus:ring-[#d2691e]">
                    <option value="" disabled>Choisir une classe</option>
                    <option v-for="c in planComptable.classes" :key="c.classe_number" :value="c.classe_number">
                      {{ c.classe_number }} - {{ c.name }}
                    </option>
                  </select>
                </div>
                <div>
                  <label class="block font-semibold text-[#5a2d0c]">Sous-classe :</label>
                  <select v-model="form.sous_classe" @change="onSousClasseChange"
                    class="w-full p-2 rounded border border-[#d4b89c] bg-[#fff8f0] focus:outline-none focus:ring-2 focus:ring-[#d2691e]">
                    <option value="" disabled>Choisir une sous-classe</option>
                    <option v-for="sc in sousClassesDisponibles" :key="sc.number" :value="sc.number">
                      {{ sc.number }} - {{ sc.name }}
                    </option>
                  </select>
                </div>
                <div>
                  <label class="block font-semibold text-[#5a2d0c]">Compte :</label>
                  <select v-model="form.compte" @change="onCompteChange"
                    class="w-full p-2 rounded border border-[#d4b89c] bg-[#fff8f0] focus:outline-none focus:ring-2 focus:ring-[#d2691e]">
                    <option value="" disabled>Choisir un compte</option>
                    <option v-for="c in comptesDisponibles" :key="c.number" :value="c.number">
                      {{ c.number }} - {{ c.name }}
                    </option>
                  </select>
                </div>
                <div>
                  <label class="block font-semibold text-[#5a2d0c]">Sous-compte :</label>
                  <select v-model="form.sous_compte" @change="onSousCompteChange"
                    class="w-full p-2 rounded border border-[#d4b89c] bg-[#fff8f0] focus:outline-none focus:ring-2 focus:ring-[#d2691e]">
                    <option value="" disabled>Choisir un sous-compte</option>
                    <option v-for="sc in sousComptesDisponibles" :key="sc.number" :value="sc.number">
                      {{ sc.number }} - {{ sc.name }}
                    </option>
                  </select>
                </div>
              </div>

              <label class="inline-flex items-center gap-2">
                <input type="checkbox" v-model="form.reconcile" class="rounded border-gray-300" />
                Rapprochement
              </label>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label class="block font-semibold text-[#5a2d0c]">Taxes :</label>
                  <select v-model="form.taxes" multiple class="w-full p-2 rounded border border-[#d4b89c] bg-[#fff8f0] focus:outline-none focus:ring-2 focus:ring-[#d2691e]">
                    <option v-for="t in taxes" :key="t.id" :value="t.id">{{ t.name }}</option>
                  </select>
                </div>
                <div>
                  <label class="block font-semibold text-[#5a2d0c]">Tags :</label>
                  <select v-model="form.tags" multiple class="w-full p-2 rounded border border-[#d4b89c] bg-[#fff8f0] focus:outline-none focus:ring-2 focus:ring-[#d2691e]">
                    <option v-for="tag in tags" :key="tag.id" :value="tag.id">{{ tag.name }}</option>
                  </select>
                </div>
              </div>

              <div v-if="requiresPartner(form.account_type)">
                <label class="block font-semibold text-[#5a2d0c]">Partenaire :</label>
                <select v-model="form.partner" class="w-full p-2 rounded border border-[#d4b89c] bg-[#fff8f0] focus:outline-none focus:ring-2 focus:ring-[#d2691e]">
                  <option value="" disabled hidden>Choisir un partenaire</option>
                  <option v-for="p in partners" :key="p.id" :value="p.id">{{ p.name }}</option>
                </select>
              </div>

              <textarea v-model="form.note" placeholder="Note (facultatif)"
                class="w-full p-2 rounded border border-[#d4b89c] bg-[#fff8f0] focus:outline-none focus:ring-2 focus:ring-[#d2691e]"></textarea>

              <div class="flex justify-end gap-3">
                <button type="submit" class="bg-[#a0522d] text-white font-bold px-6 py-2 rounded-xl hover:bg-[#d2691e] transition-colors">
                  {{ form.id ? 'Modifier' : 'Ajouter' }}
                </button>
                <button type="button" @click="closeModal" class="bg-gray-400 text-white font-bold px-6 py-2 rounded-xl hover:bg-gray-500 transition-colors">
                  Annuler
                </button>
              </div>
            </form>
          </div>
        </div>
      </transition>

      <!-- Modal Écritures -->
      <transition name="fade">
        <div v-if="ecritureModalVisible" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div class="bg-white rounded-2xl w-full max-w-4xl p-6 shadow-2xl max-h-[90vh] overflow-y-auto relative">
            <button @click="ecritureModalVisible=false" class="absolute top-4 right-4 p-1 rounded hover:bg-gray-200">
              <X class="w-5 h-5" />
            </button>
            <h3 class="text-2xl font-bold text-[#5a2d0c] mb-4">
              Écritures du compte {{ selectedCompte?.name }}
            </h3>
            <table class="min-w-full bg-white rounded-xl shadow overflow-hidden">
              <thead class="bg-[#8b4513] text-white">
                <tr>
                  <th class="py-2 px-4">Date</th>
                  <th class="py-2 px-4">Libellé</th>
                  <th class="py-2 px-4">Débit</th>
                  <th class="py-2 px-4">Crédit</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="e in ecritures" :key="e.id" class="hover:bg-[#fce8d8] transition-colors">
                  <td class="py-2 px-4">{{ e.date }}</td>
                  <td class="py-2 px-4">{{ e.label }}</td>
                  <td class="py-2 px-4">{{ e.debit }}</td>
                  <td class="py-2 px-4">{{ e.credit }}</td>
                </tr>
                <tr v-if="ecritures.length===0">
                  <td colspan="4" class="text-center py-4 text-gray-500">Aucune écriture disponible</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import api from '../axios.js';
import plan_comptable_general_2005 from '../../compte.json';
import { PlusCircle, Search, Edit3, BookOpen, Trash2, X, Package } from 'lucide-vue-next';
export default {
  components: { PlusCircle, Search, Edit3, BookOpen, Trash2, X, Package },


  data() {
    return {
    searchTerm: '',
    planComptable: plan_comptable_general_2005.plan_comptable_general_2005,
      comptes: [],
      sousClassesDisponibles: [],
      comptesDisponibles: [],
      sousComptesDisponibles: [],
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
      partner: null,
      classe: '',
        sous_classe: '',
        compte: '',
        sous_compte: ''
    },
    currencies: [],
    taxes: [],
    tags: [],
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
  computed: {
  filteredComptes() {
    if (!this.searchTerm) return this.comptes;
    const term = this.searchTerm.toLowerCase();
    return this.comptes.filter(c =>
      c.code.toLowerCase().includes(term) ||
      c.name.toLowerCase().includes(term) ||
      (c.account_type && c.account_type.toLowerCase().includes(term))
    );
  }
},
  methods: {
  requiresPartner(type) {
      // Les types qui nécessitent un partenaire
      return ["asset_receivable", "liability_payable"].includes(type);
    },
    formatDate(date) {
    if (!date) return "-";
    return new Date(date).toLocaleDateString("fr-FR", {
      year: "numeric",
      month: "short",
      day: "2-digit"
    });
    },
    formatAmount(value) {
    if (value == null) return "-";
    return new Intl.NumberFormat("fr-FR", { style: "currency", currency: "EUR" }).format(value);
  },
    onClasseChange() {
      const classe = this.planComptable.classes.find(c => c.classe_number === this.form.classe);
      this.sousClassesDisponibles = classe ? classe.accounts : [];
      this.form.sous_classe = '';
      this.comptesDisponibles = [];
      this.sousComptesDisponibles = [];
    },
    onSousClasseChange() {
      const sc = this.sousClassesDisponibles.find(s => s.number === this.form.sous_classe);
      this.comptesDisponibles = sc ? sc.subaccounts : [];
      this.form.compte = '';
      this.sousComptesDisponibles = [];
    },
    onCompteChange() {
      const compte = this.comptesDisponibles.find(c => c.number === this.form.compte);
      this.sousComptesDisponibles = compte ? compte.details : [];
      this.form.sous_compte = '';
    },
    onSousCompteChange() {
      const sousCompte = this.sousComptesDisponibles.find(s => s.number === this.form.sous_compte);
      if (sousCompte) {
        this.form.code = sousCompte.number;
        this.form.name = sousCompte.name;
      }
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
      partner: compte.partner || null,
      classe: compte.classe || '',
      sous_classe: compte.sous_classe || '',
      compte: compte.compte || '',
      sous_compte: compte.sous_compte || ''
    };
    if (this.form.classe) {
      const classe = this.planComptable.classes.find(c => c.classe_number === this.form.classe);
      this.sousClassesDisponibles = classe ? classe.accounts : [];
    }
    if (this.form.sous_classe) {
      const sc = this.sousClassesDisponibles.find(s => s.number === this.form.sous_classe);
      this.comptesDisponibles = sc ? sc.subaccounts : [];
    }
    if (this.form.compte) {
      const c = this.comptesDisponibles.find(c => c.number === this.form.compte);
      this.sousComptesDisponibles = c ? c.details : [];
    }
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
      partner: null,
      classe: '',
      sous_classe: '',
      compte: '',
      sous_compte: ''
    };
    this.modalVisible = true;
    this.sousClassesDisponibles = [];
    this.comptesDisponibles = [];
    this.sousComptesDisponibles = [];
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

    if (!this.form.code || !this.form.name || !this.form.account_type) {
      alert("Veuillez remplir tous les champs obligatoires !");
      return;
    }

    const payload = {
      code: this.form.code,
      name: this.form.name,
      account_type: this.form.account_type,
      currency: this.form.currency || null,
      reconcile: this.form.reconcile,
      note: this.form.note,
      taxes: Array.isArray(this.form.taxes) ? this.form.taxes : [],
      tags: Array.isArray(this.form.tags) ? this.form.tags : [],
      partner: this.form.partner || null,
      classe: this.form.classe || null,
      sous_classe: this.form.sous_classe || null,
      compte: this.form.compte || null,
      sous_compte: this.form.sous_compte || null
    };

    if (this.form.id) {
      await api.put(`/api/comptes/${this.form.id}/`, payload);
    } else {
      await api.post('/api/comptes/', payload);
    }

    await this.fetchComptes();
    this.closeModal();

  } catch (e) {
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
  } catch(e) {
    console.error("Erreur lors du chargement des écritures:", e);
    alert("Erreur lors du chargement des écritures : " + (e.response?.data?.message || e.message));
  }
}
  },
  mounted() {
    this.fetchComptes();
    this.fetchSelects();
  }
}
</script>
<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity .2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>