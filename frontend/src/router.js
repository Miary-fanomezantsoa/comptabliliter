import { createRouter, createWebHistory } from 'vue-router'
import LayoutLModern from "@/components/LayoutLModern.vue";
import Login from './components/Login.vue'
import Dashboard from './components/Dashboard.vue'
import Comptes from './components/CompteComptable.vue'
import Partners from "./components/PartnerForm.vue"
import PartnerList from './components/PartnerList.vue';
import JournalManager from './components/JournalManager.vue';
import CommandePayment from './components/CommandePayment.vue';
import Balance from './components/balance.vue';
import Livre from './components/GeneralLedger.vue';
import Index from './components/index.vue';
import User from './components/User.vue';
import Paramettre from './components/Parametre.vue'
import produit from './components/ProductView.vue'
import invoice from './components/InvoiceClient.vue'
import chatbot from './components/Chatbot.vue'


const routes = [
  { path: '/', redirect: '/login' },

  { path: '/login', name: 'Login', component: Login },

  // Layout parent pour toutes les pages connectées
  {
    path: '/',
    component: LayoutLModern,
    meta: { requiresAuth: true },
    children: [
      {path: 'chatbot', name: 'chatbot',component: chatbot},
      {path: 'produit', name: 'produit',component: produit},
      {path: 'Paramettre', name: 'Paramettre',component: Paramettre},
      {path: 'User', name: 'User',component: User},
      { path: 'dashboard', name: 'Dashboard', component: Dashboard },
      { path: 'comptes', name: 'Comptes', component: Comptes },
      { path: 'partners/:partnerId?', name: 'Partners', component: Partners },
      { path: 'partners-list', name: 'PartnerList', component: PartnerList },
      { path: 'journals', name: 'Journals', component: JournalManager },
      { path: 'commande&payment', name: 'CommandePayment', component: CommandePayment },
      { path: 'balance', name: 'Balance', component: Balance },
      { path: 'livre', name: 'Livre', component: Livre },
      { path: '', name: 'Index', component: Index },
      {path: 'invoice', name: 'invoice', component:invoice},
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

function isLoggedIn() {
  const token = localStorage.getItem('access_token');
  if (!token) return false;
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return Date.now() < payload.exp * 1000;
  } catch (e) {
    return false;
  }
}

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !isLoggedIn()) next({ name: 'Login' });
  else if (to.name === 'Login' && isLoggedIn()) next({ name: 'Dashboard' });
  else next();
});

export default router;
