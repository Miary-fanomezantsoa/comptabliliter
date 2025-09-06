<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <div class="max-w-5xl mx-auto bg-white shadow-lg rounded-xl p-6 space-y-6">

      <h1 class="text-3xl font-bold text-gray-800"> Gestion Produits</h1>

      <!-- Bouton Ajouter produit -->
      <button @click="showForm = !showForm"
        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition flex items-center gap-2">
  <component :is="showForm ? X : PlusCircle" class="w-5 h-5"/>
  {{ showForm ? "Annuler" : "Ajouter Produit" }}
</button>


      <!-- Formulaire d'ajout produit -->
      <form v-if="showForm" @submit.prevent="addProduct" class="space-y-4 bg-gray-50 p-4 rounded-lg shadow">
        <div>
          <label class="block text-sm font-medium text-gray-700">Nom du produit</label>
          <input v-model="newProduct.name" type="text"
            class="mt-1 block w-full border rounded-lg p-2 focus:ring focus:ring-blue-300" required />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Catégorie</label>
          <select v-model="newProduct.category"
            class="mt-1 block w-full border rounded-lg p-2 focus:ring focus:ring-blue-300">
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
          </select>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Prix unitaire</label>
            <input v-model="newProduct.unit_price" type="number" step="0.01"
              class="mt-1 block w-full border rounded-lg p-2 focus:ring focus:ring-blue-300" required />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Quantité</label>
            <input v-model="newProduct.quantity" type="number"
              class="mt-1 block w-full border rounded-lg p-2 focus:ring focus:ring-blue-300" />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Description</label>
          <textarea v-model="newProduct.description"
            class="mt-1 block w-full border rounded-lg p-2 focus:ring focus:ring-blue-300"></textarea>
        </div>

        <button type="submit"
        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition flex items-center gap-2">
  <PlusCircle class="w-5 h-5"/>
  Ajouter Produit
</button>
</form>


      <!-- Recherche -->
      <div class="relative mt-4 w-full">
  <input v-model="searchQuery" type="text" placeholder="Rechercher par nom ou catégorie"
         class="w-full border rounded-lg p-2 pl-10 focus:ring focus:ring-blue-300"/>
  <Search class="w-5 h-5 absolute left-2 top-1/2 transform -translate-y-1/2 text-blue-500"/>
</div>


      <!-- Liste des produits -->
      <h2 class="text-2xl font-semibold text-gray-800 mt-4 mb-2">Liste des Produits</h2>
      <div class="overflow-x-auto">
        <table class="w-full border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-200">
            <tr>
              <th class="px-4 py-2 text-left">Nom</th>
              <th class="px-4 py-2 text-left">Catégorie</th>
              <th class="px-4 py-2 text-left">Prix</th>
              <th class="px-4 py-2 text-left">Quantité</th>
              <th class="px-4 py-2 text-left">Description</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="prod in filteredProducts" :key="prod.id" class="border-b hover:bg-gray-50">
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
