<script setup>
import { ref, onMounted } from 'vue'
import api from '../axios'

const activeTab = ref('currency')


const currencies = ref([])
const taxes = ref([])
const tags = ref([])
const category = ref([])
const currencyForm = ref({ id: null, name: '', symbol: '', code: '' })
const taxForm = ref({ id: null, name: '', rate: '' })
const tagForm = ref({ id: null, name: '' })
const categoryForm = ref({ id: null, name: '' })

const isEditingCurrency = ref(false)
const isEditingTax = ref(false)
const isEditingTag = ref(false)
const isEditingCategory = ref(false)

const fetchCurrencies = async () => {
  try {
    const res = await api.get('/api/currencies/')
    currencies.value = res.data
  } catch (err) { console.error(err) }
}

const fetchCategories = async () => {
  try {
    const res = await api.get('/api/category/')
    category.value = res.data
  } catch (err) { console.error(err) }
}
const fetchTaxes = async () => {
  try {
    const res = await api.get('/api/taxes/')
    taxes.value = res.data
  } catch (err) { console.error(err) }
}

const fetchTags = async () => {
  try {
    const res = await api.get('/api/account-tags/')
    tags.value = res.data
  } catch (err) { console.error(err) }
}

const fetchAll = () => {
  fetchCurrencies()
  fetchTaxes()
  fetchTags()
  fetchCategories()
}

onMounted(fetchAll)

// ---- CRUD FUNCTIONS ----
const saveItem = async (type) => {
  try {
    if (type === 'currency') {
      if (isEditingCurrency.value) {
        await api.put(`/api/currencies/${currencyForm.value.id}/`, currencyForm.value)
        isEditingCurrency.value = false
      } else {
        await api.post('/api/currencies/', currencyForm.value)
      }
      currencyForm.value = { id: null, name: '', symbol: '', code: '' }
      fetchCurrencies()
    }else if (type === 'category') {
      if (isEditingCategory.value) {
        await api.put(`/api/category/${categoryForm.value.id}/`, categoryForm.value)
        isEditingCategory.value = false
      } else {
        await api.post('/api/category/', categoryForm.value)
      }
      categoryForm.value = { id: null, name: '' }
      fetchCategories()
    }else if (type === 'tax') {
      if (isEditingTax.value) {
        await api.put(`/api/taxes/${taxForm.value.id}/`, taxForm.value)
        isEditingTax.value = false
      } else {
        await api.post('/api/taxes/', taxForm.value)
      }
      taxForm.value = { id: null, name: '', rate: '' }
      fetchTaxes()
    } else if (type === 'tag') {
      if (isEditingTag.value) {
        await api.put(`/api/account-tags/${tagForm.value.id}/`, tagForm.value)
        isEditingTag.value = false
      } else {
        await api.post('/api/account-tags/', tagForm.value)
      }
      tagForm.value = { id: null, name: '' }
      fetchTags()
    }
  } catch (err) {
    console.error(err)
  }
}

const editItem = (type, item) => {
  if (type === 'currency') { currencyForm.value = { ...item }; isEditingCurrency.value = true }
  if (type === 'tax') { taxForm.value = { ...item }; isEditingTax.value = true }
  if (type === 'tag') { tagForm.value = { ...item }; isEditingTag.value = true }
  if (type === 'category') {categoryForm.value = { ...item };isEditingCategory.value = true }
}

const deleteItem = async (type, id) => {
  try {
    await api.delete(`/api/${type}/${id}/`)
    fetchAll()
  } catch (err) { console.error(err) }
}

const cancelEdit = (type) => {
  if (type === 'currency') { currencyForm.value = { id: null, name: '', symbol: '', code: '' }; isEditingCurrency.value = false }
  if (type === 'tax') { taxForm.value = { id: null, name: '', rate: '' }; isEditingTax.value = false }
  if (type === 'tag') { tagForm.value = { id: null, name: '' }; isEditingTag.value = false }
  if (type === 'category') {
    categoryForm.value = { id: null, name: '' }
    isEditingCategory.value = false
  }
}
</script>

<template>
<div class="max-w-6xl mx-auto p-6 bg-[#fdfaf7] shadow rounded-lg">
  <h2 class="text-2xl sm:text-3xl font-bold mb-6 text-center text-[#4e342e]">Configuration</h2>

  <!-- Onglets -->
  <div class="flex gap-2 mb-4">
    <button :class="activeTab==='currency'? 'bg-[#6d4c41] text-white' : 'bg-[#d7ccc8] text-[#4e342e]'"
            @click="activeTab='currency'" class="px-4 py-2 rounded">Monnaies</button>
    <button :class="activeTab==='tax'? 'bg-[#6d4c41] text-white' : 'bg-[#d7ccc8] text-[#4e342e]'"
            @click="activeTab='tax'" class="px-4 py-2 rounded">Taxes</button>
    <button :class="activeTab==='tag'? 'bg-[#6d4c41] text-white' : 'bg-[#d7ccc8] text-[#4e342e]'"
            @click="activeTab='tag'" class="px-4 py-2 rounded">Tags de comptes</button>
    <button :class="activeTab==='category'? 'bg-[#6d4c41] text-white' : 'bg-[#d7ccc8] text-[#4e342e]'"
            @click="activeTab='category'" class="px-4 py-2 rounded">Catégories de produit</button>
  </div>

  <!-- ---- Currency ---- -->
  <div v-if="activeTab==='currency'" class="space-y-4">
    <form @submit.prevent="saveItem('currency')" class="grid grid-cols-1 sm:grid-cols-4 gap-4">
      <input v-model="currencyForm.name" placeholder="Nom" class="border rounded px-3 py-2 focus:ring-2 focus:ring-[#a1887f]"/>
      <input v-model="currencyForm.symbol" placeholder="Symbole" class="border rounded px-3 py-2 focus:ring-2 focus:ring-[#a1887f]"/>
      <input v-model="currencyForm.code" placeholder="Code" class="border rounded px-3 py-2 focus:ring-2 focus:ring-[#a1887f]"/>
      <div class="flex gap-2">
        <button type="submit" class="bg-[#6d4c41] text-white px-4 py-2 rounded hover:bg-[#5d4037]">
          {{ isEditingCurrency ? 'Mettre à jour' : 'Créer' }}
        </button>
        <button type="button" @click="cancelEdit('currency')" v-if="isEditingCurrency"
                class="bg-[#8d6e63] text-white px-4 py-2 rounded hover:bg-[#795548]">Annuler</button>
      </div>
    </form>

    <div class="overflow-x-auto">
      <table class="w-full border border-[#d7ccc8] table-auto">
        <thead class="bg-[#efebe9] text-[#4e342e]">
          <tr>
            <th class="border px-4 py-2">Nom</th>
            <th class="border px-4 py-2">Symbole</th>
            <th class="border px-4 py-2">Code</th>
            <th class="border px-4 py-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in currencies" :key="c.id" class="hover:bg-[#fbe9e7]">
            <td class="border px-4 py-2">{{ c.name }}</td>
            <td class="border px-4 py-2">{{ c.symbol }}</td>
            <td class="border px-4 py-2">{{ c.code }}</td>
            <td class="border px-4 py-2 flex gap-2">
              <button @click="editItem('currency', c)" class="bg-[#a1887f] text-white px-2 py-1 rounded hover:bg-[#8d6e63]">Éditer</button>
              <button @click="deleteItem('currencies', c.id)" class="bg-[#d84315] text-white px-2 py-1 rounded hover:bg-[#bf360c]">Supprimer</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- ---- Tax ---- -->
  <div v-if="activeTab==='tax'" class="space-y-4">
    <form @submit.prevent="saveItem('tax')" class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <input v-model="taxForm.name" placeholder="Nom" class="border rounded px-3 py-2 focus:ring-2 focus:ring-[#a1887f]"/>
      <input v-model="taxForm.rate" placeholder="Taux (%)" type="number" class="border rounded px-3 py-2 focus:ring-2 focus:ring-[#a1887f]"/>
      <div class="flex gap-2">
        <button type="submit" class="bg-[#6d4c41] text-white px-4 py-2 rounded hover:bg-[#5d4037]">{{ isEditingTax ? 'Mettre à jour' : 'Créer' }}</button>
        <button type="button" @click="cancelEdit('tax')" v-if="isEditingTax" class="bg-[#8d6e63] text-white px-4 py-2 rounded hover:bg-[#795548]">Annuler</button>
      </div>
    </form>
    <div class="overflow-x-auto">
      <table class="w-full border border-[#d7ccc8] table-auto">
        <thead class="bg-[#efebe9] text-[#4e342e]">
          <tr>
            <th class="border px-4 py-2">Nom</th>
            <th class="border px-4 py-2">Taux (%)</th>
            <th class="border px-4 py-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in taxes" :key="t.id" class="hover:bg-[#fbe9e7]">
            <td class="border px-4 py-2">{{ t.name }}</td>
            <td class="border px-4 py-2">{{ t.rate }}</td>
            <td class="border px-4 py-2 flex gap-2">
              <button @click="editItem('tax', t)" class="bg-[#a1887f] text-white px-2 py-1 rounded hover:bg-[#8d6e63]">Éditer</button>
              <button @click="deleteItem('taxes', t.id)" class="bg-[#d84315] text-white px-2 py-1 rounded hover:bg-[#bf360c]">Supprimer</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- ---- Account Tag ---- -->
  <div v-if="activeTab==='tag'" class="space-y-4">
    <form @submit.prevent="saveItem('tag')" class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <input v-model="tagForm.name" placeholder="Nom" class="border rounded px-3 py-2 focus:ring-2 focus:ring-[#a1887f]"/>
      <div class="flex gap-2">
        <button type="submit" class="bg-[#6d4c41] text-white px-4 py-2 rounded hover:bg-[#5d4037]">{{ isEditingTag ? 'Mettre à jour' : 'Créer' }}</button>
        <button type="button" @click="cancelEdit('tag')" v-if="isEditingTag" class="bg-[#8d6e63] text-white px-4 py-2 rounded hover:bg-[#795548]">Annuler</button>
      </div>
    </form>
    <div class="overflow-x-auto">
      <table class="w-full border border-[#d7ccc8] table-auto">
        <thead class="bg-[#efebe9] text-[#4e342e]">
          <tr>
            <th class="border px-4 py-2">Nom</th>
            <th class="border px-4 py-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="tag in tags" :key="tag.id" class="hover:bg-[#fbe9e7]">
            <td class="border px-4 py-2">{{ tag.name }}</td>
            <td class="border px-4 py-2 flex gap-2">
              <button @click="editItem('tag', tag)" class="bg-[#a1887f] text-white px-2 py-1 rounded hover:bg-[#8d6e63]">Éditer</button>
              <button @click="deleteItem('account-tags', tag.id)" class="bg-[#d84315] text-white px-2 py-1 rounded hover:bg-[#bf360c]">Supprimer</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- ---- Category ---- -->
  <div v-if="activeTab==='category'" class="space-y-4">
    <form @submit.prevent="saveItem('category')" class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <input v-model="categoryForm.name" placeholder="Nom de la catégorie" class="border rounded px-3 py-2 focus:ring-2 focus:ring-[#a1887f]"/>
      <div class="flex gap-2">
        <button type="submit" class="bg-[#6d4c41] text-white px-4 py-2 rounded hover:bg-[#5d4037]">{{ isEditingCategory ? 'Mettre à jour' : 'Créer' }}</button>
        <button type="button" @click="cancelEdit('category')" v-if="isEditingCategory" class="bg-[#8d6e63] text-white px-4 py-2 rounded hover:bg-[#795548]">Annuler</button>
      </div>
    </form>
    <div class="overflow-x-auto">
      <table class="w-full border border-[#d7ccc8] table-auto">
        <thead class="bg-[#efebe9] text-[#4e342e]">
          <tr>
            <th class="border px-4 py-2">Nom</th>
            <th class="border px-4 py-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="cat in category" :key="cat.id" class="hover:bg-[#fbe9e7]">
            <td class="border px-4 py-2">{{ cat.name }}</td>
            <td class="border px-4 py-2 flex gap-2">
              <button @click="editItem('category', cat)" class="bg-[#a1887f] text-white px-2 py-1 rounded hover:bg-[#8d6e63]">Éditer</button>
              <button @click="deleteItem('category', cat.id)" class="bg-[#d84315] text-white px-2 py-1 rounded hover:bg-[#bf360c]">Supprimer</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</div>
</template>
