<template>
  <header class="bg-gradient-to-r from-[#4d3a33] to-[#795548] h-16 flex items-center justify-between px-6 shadow-lg sticky top-0 z-50">
    <!-- Logo et titre -->
    <div class="flex items-center gap-3">
      <img src="/logo_rm_bg.png" alt="Logo" class="h-10 w-10 rounded-full shadow-md transition-transform duration-500 hover:scale-110 hover:-rotate-3"/>
<span class="text-white text-xl font-bold select-none">Chocolaterie Robert</span>
    </div>

    <!-- Bouton Déconnexion -->
    <button @click="logout"
            class="bg-[#c06b3e] text-white px-4 py-2 rounded-xl font-semibold shadow-lg hover:bg-[#a0522d] hover:shadow-xl transition duration-300 transform hover:scale-105">
      🔒 Se déconnecter
    </button>
  </header>
</template>

<script>
export default {
  name: "HeaderWithNav",
  methods: {
    logout() {
      // Supprime les tokens
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      // Redirection vers la page de login
      this.$router.push({ name: "Login" });
    }
  }
};
</script>

<style scoped>
/* Optionnel : ajouter un petit effet sur le texte du titre */
header span {
  transition: color 0.3s;
}
header span:hover {
  color: #facc15; /* jaune poussin */
}
</style>
