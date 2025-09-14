<template>
  <div class="min-h-screen bg-gradient-to-br from-[#f8f4f1] to-[#ede0d4] p-6">
    <div class="max-w-5xl mx-auto bg-[#fff8f2] shadow-xl rounded-xl p-6 space-y-6 border border-[#e6ccb2]">

      <h1 class="text-3xl font-bold text-[#5c3d2e]"> Gestion Produits</h1>

      <!-- Bouton Ajouter produit -->
      <button @click="showForm = !showForm"
        class="px-4 py-2 bg-[#7f5539] text-white rounded-lg hover:bg-[#9c6644] transition flex items-center gap-2 shadow-md">
        <X v-if="showForm" class="w-5 h-5"/>
        <PlusCircle v-else class="w-5 h-5"/>
        {{ showForm ? "Annuler" : "Ajouter Produit" }}
      </button>

      <!-- Formulaire d'ajout produit -->
      <form v-if="showForm" @submit.prevent="addProduct" class="space-y-4 bg-[#faf3e9] p-4 rounded-lg shadow-inner border border-[#ddb892]">
        <div>
          <label class="block text-sm font-medium text-[#6c4a3c]">Nom du produit</label>
          <input v-model="newProduct.name" type="text"
            class="mt-1 block w-full border border-[#e6ccb2] rounded-lg p-2 focus:ring focus:ring-[#b08968]" required />
        </div>

        <div>
          <label class="block text-sm font-medium text-[#6c4a3c]">Catégorie</label>
          <select v-model="newProduct.category"
            class="mt-1 block w-full border border-[#e6ccb2] rounded-lg p-2 focus:ring focus:ring-[#b08968]">
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
          </select>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-[#6c4a3c]">Prix unitaire</label>
            <input v-model="newProduct.unit_price" type="number" step="0.01"
              class="mt-1 block w-full border border-[#e6ccb2] rounded-lg p-2 focus:ring focus:ring-[#b08968]" required />
          </div>

          <div>
            <label class="block text-sm font-medium text-[#6c4a3c]">Quantité</label>
            <input v-model="newProduct.quantity" type="number"
              class="mt-1 block w-full border border-[#e6ccb2] rounded-lg p-2 focus:ring focus:ring-[#b08968]" />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-[#6c4a3c]">Description</label>
          <textarea v-model="newProduct.description"
            class="mt-1 block w-full border border-[#e6ccb2] rounded-lg p-2 focus:ring focus:ring-[#b08968]"></textarea>
        </div>

        <button type="submit"
        class="px-4 py-2 bg-[#7f5539] text-white rounded-lg hover:bg-[#9c6644] transition flex items-center gap-2 shadow-md">
          <PlusCircle class="w-5 h-5"/>
          Ajouter Produit
        </button>
      </form>

      <!-- Recherche -->
      <div class="relative mt-4 w-full">
        <input v-model="searchQuery" type="text" placeholder="Rechercher par nom ou catégorie"
          class="w-full border border-[#e6ccb2] rounded-lg p-2 pl-10 focus:ring focus:ring-[#b08968] bg-[#fffdf9]"/>
        <Search class="w-5 h-5 absolute left-2 top-1/2 transform -translate-y-1/2 text-[#9c6644]"/>
      </div>

      <!-- Liste des produits -->
      <h2 class="text-2xl font-semibold text-[#5c3d2e] mt-4 mb-2">Liste des Produits</h2>
      <div class="overflow-x-auto">
        <table class="w-full border border-[#e6ccb2] rounded-lg overflow-hidden text-[#3e2c23]">
          <thead class="bg-[#e6ccb2] text-[#3e2c23]">
            <tr>
              <th class="px-4 py-2 text-left">Nom</th>
              <th class="px-4 py-2 text-left">Catégorie</th>
              <th class="px-4 py-2 text-left">Prix</th>
              <th class="px-4 py-2 text-left">Quantité</th>
              <th class="px-4 py-2 text-left">Description</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="prod in filteredProducts" :key="prod.id" class="border-b hover:bg-[#f0e1d2]">
              <td class="px-4 py-2">{{ prod.name }}</td>
              <td class="px-4 py-2">{{ prod.category_name }}</td>
              <td class="px-4 py-2">{{ prod.unit_price }} Ar</td>
              <td class="px-4 py-2">{{ prod.quantity }}</td>
              <td class="px-4 py-2">{{ prod.description }}</td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
  </div>
</template>


<script>
import api from "../axios";
import { PlusCircle, Search, Edit, Trash2, X } from "lucide-vue-next";


export default {
components: {
  PlusCircle, Search, Edit, Trash2, X
},

  name: "ProductView",

  data() {
    return {

      products: [],
      categories: [],
      searchQuery: "",
      showForm: false,
      newProduct: {
        name: "",
        category: null,
        unit_price: "",
        quantity: 0,
        description: "",
      },
    };
  },
  computed: {
    filteredProducts() {
      const query = this.searchQuery.toLowerCase();
      return this.products.filter(prod =>
        prod.name.toLowerCase().includes(query) ||
        (prod.category_name && prod.category_name.toLowerCase().includes(query))
      );
    }
  },
  methods: {
    async fetchProducts() {
      const res = await api.get("api/products/");
      this.products = res.data;
    },
    async fetchCategories() {
      const res = await api.get("api/category/");
      this.categories = res.data;
    },
    async addProduct() {
      await api.post("api/products/", this.newProduct);
      this.newProduct = { name: "", category: null, unit_price: "", quantity: 0, description: "" };
      this.fetchProducts();
      this.showForm = false; // Masquer le formulaire après ajout
    },
  },
  mounted() {
    this.fetchProducts();
    this.fetchCategories();
  },
};
</script>
