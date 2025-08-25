<template>
  <div class="dashboard">

    <!-- Cartes d'information -->
    <section class="stats">
      <div class="card" v-for="item in statsList" :key="item.title" :class="item.color">
        <h2>{{ item.icon }} {{ item.title }}</h2>
        <p>{{ item.value }} {{ item.label }}</p>
        <button @click="item.action()">Voir</button>
      </div>
    </section>

    <!-- Actions rapides -->
    <section class="quick-actions">
      <h2>⚡ Actions rapides</h2>
      <div class="actions-grid">
        <button @click="goToComptes">📂 Gestion des comptes</button>
        <button @click="goToJournaux">🧾 Gestion des journaux</button>
        <button @click="goToReports">📊 Rapports</button>
        <button @click="goToPartners">🤝 Créer un partenaire</button>
      </div>
    </section>

  </div>
</template>

<script>
import api from "../axios";

export default {
  name: "Dashboard",
  data() {
    return {
      user: null,
      stats: {
        comptes: 0,
        journaux: 0
      },
      statsList: []
    };
  },
  async mounted() {
    await this.fetchUser();
    await this.fetchStats();
  },
  methods: {
    async fetchUser() {
      try {
        const response = await api.get("/api/user/");
        this.user = response.data;
      } catch {
        this.user = null;
      }
    },
    async fetchStats() {
      try {
        const comptesRes = await api.get("/api/comptes/");
        const journauxRes = await api.get("/api/journals/");
        this.stats.comptes = comptesRes.data.length;
        this.stats.journaux = journauxRes.data.length;

        this.statsList = [
          { title: "Comptes", value: this.stats.comptes, label: "comptes", icon: "💼", action: this.goToComptes, color: "card-brown" },
          { title: "Journaux", value: this.stats.journaux, label: "journals", icon: "🧾", action: this.goToJournaux, color: "card-chocolate" }
        ];
      } catch {
        this.stats = { comptes: 0, journaux: 0 };
      }
    },
    logout() {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      this.$router.push({ name: "Login" });
    },
    goToComptes() {
      this.$router.push({ name: "Comptes" });
    },
    goToJournaux() {
      this.$router.push({ name: "Journals" });
    },
    goToReports() {
      this.$router.push({ name: "Rapports" });
    },
    goToPartners() {
      this.$router.push({ name: "Partners" });
    }
  }
};
</script>

<style scoped>
.dashboard {
  padding: 2rem;
  font-family: 'Roboto', sans-serif;
  background: #fdf5f0;
}

/* Stats cards */
.stats {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
  margin-bottom: 2rem;
}

.card {
  flex: 1;
  min-width: 220px;
  border-radius: 12px;
  padding: 1.2rem;
  color: #fff;
  box-shadow: 0 4px 15px rgba(0,0,0,0.15);
  transition: transform 0.3s, box-shadow 0.3s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.25);
}

.card h2 {
  margin-bottom: 0.5rem;
}

.card button {
  background: #fff;
  color: #4b2e2b;
  padding: 0.4rem 0.8rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s;
}

.card button:hover {
  background: #f3e1d2;
}

/* Couleurs chocolat */
.card-brown { background: #8b4513; }
.card-chocolate { background: #d2691e; }

/* Actions rapides */
.quick-actions h2 {
  margin-bottom: 1rem;
  color: #4b2e2b;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
}

.actions-grid button {
  background: #d2691e;
  color: white;
  padding: 0.8rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.actions-grid button:hover {
  background: #8b4513;
}
</style>
