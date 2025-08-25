import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(router)      // Installer le router AVANT de monter l'app
app.mount('#app')    // Monter l'app UNE seule fois
