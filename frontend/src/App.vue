<template>
  <div id="app">
    <!-- Header affiché sauf si on est sur /login -->
    <Header v-if="$route.path !== '/login'" />


    <router-view />
  </div>
</template>

<script>
import GeminiChat from './components/gemini.vue'; // assure-toi que le nom du fichier est correct
import JournalManager from './components/JournalManager.vue'
import index from './components/index.vue'
import Header from './components/Header.vue'

export default {
  components: { GeminiChat},
  name: 'App'
}
</script>
