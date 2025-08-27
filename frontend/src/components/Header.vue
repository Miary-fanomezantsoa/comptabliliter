<template>
  <header class="app-header">
    <div class="header-left">
      <img src="/logo_rm_bg.png" alt="Logo Chocolaterie" class="logo" />
      <span class="company-name">Chocolaterie Robert</span>
    </div>

    <nav class="nav-links">
      <router-link to="/dashboard" class="nav-item">Dashboard</router-link>
      <router-link to="/comptes" class="nav-item">Comptes</router-link>
      <router-link to="/journals" class="nav-item">Journal</router-link>
      <router-link to="/partners-list" class="nav-item">Partenaires</router-link>
      <router-link to="/commande&payment" class="nav-item">commande et payment</router-link>
      <router-link to="/balance" class="nav-item">balance</router-link>
    </nav>

    <div class="header-right">
      <button @click="logout" class="logout-btn">
        <span>Se déconnecter</span>
      </button>
    </div>
  </header>
</template>

<script>
export default {
  name: "Header",
  methods: {
    logout() {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      this.$router.push({ name: "Login" });
    }
  }
};
</script>

<style scoped>
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(135deg, #4e342e, #6d4c41); /* gradient chocolat */
  padding: 10px 25px;
  color: white;
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
  position: sticky;
  top: 0;
  z-index: 100;
  transition: background 0.3s ease;
}

.app-header:hover {
  background: linear-gradient(135deg, #6d4c41, #4e342e);
}

.header-left {
  display: flex;
  align-items: center;
}

.logo {
  height: 45px;
  margin-right: 12px;
  transition: transform 0.3s;
}

.logo:hover {
  transform: scale(1.1) rotate(-5deg);
}

.company-name {
  font-size: 1.6em;
  font-weight: bold;
  font-family: 'Pacifico', cursive; /* un style gourmand */
  letter-spacing: 1px;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-item {
  color: white;
  text-decoration: none;
  font-weight: 500;
  padding: 5px 10px;
  border-radius: 6px;
  transition: all 0.3s;
}

.nav-item:hover {
  background: rgba(255,255,255,0.2);
  transform: translateY(-2px);
}

.logout-btn {
  background-color: #d84315; /* rouge chocolat */
  color: white;
  border: none;
  padding: 7px 15px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s;
}

.logout-btn:hover {
  background-color: #bf360c;
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}

/* Styles existants ... */

@media (max-width: 1024px) {
  .nav-links {
    gap: 10px;
    flex-wrap: wrap;
    justify-content: center;
    margin-top: 5px;
  }

  .company-name {
    font-size: 1.3em;
  }

  .logo {
    height: 40px;
  }

  .logout-btn {
    padding: 6px 12px;
    font-size: 0.9em;
  }
}

@media (max-width: 768px) {
  .app-header {
    flex-direction: column;
    align-items: center;
    padding: 10px 15px;
  }

  .header-left {
    flex-direction: column;
    align-items: center;
    margin-bottom: 8px;
  }

  .nav-links {
    flex-direction: column;
    gap: 8px;
    width: 100%;
    text-align: center;
  }

  .nav-item {
    width: 100%;
  }

  .header-right {
    margin-top: 8px;
  }
}

@media (max-width: 480px) {
  .company-name {
    font-size: 1.1em;
  }

  .logo {
    height: 35px;
  }

  .nav-item {
    font-size: 0.9em;
    padding: 4px 8px;
  }

  .logout-btn {
    padding: 5px 10px;
    font-size: 0.85em;
  }
}

</style>
