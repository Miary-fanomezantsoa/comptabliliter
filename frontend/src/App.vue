<template>
  <div id="app">
    <!-- Header affiché sauf si on est sur /login -->
    <Header v-if="$route.path !== '/login'" />


    <router-view />
  </div>
</template>

<script>
import Header from "./components/Header.vue";
import GeminiChat from './components/gemini.vue'; // assure-toi que le nom du fichier est correct
import JournalManager from './components/JournalManager.vue'
export default {
  components: { Header, GeminiChat },
  name: 'App'
}
</script>
