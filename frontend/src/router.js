import { createRouter, createWebHistory } from 'vue-router'
import Login from './components/Login.vue'
import Dashboard from './components/Dashboard.vue'
import Comptes from './components/CompteComptable.vue'
import Partners from "./components/PartnerForm.vue"; // <-- importe ton composant
import PartnerList from './components/PartnerList.vue';
import JournalManager from './components/JournalManager.vue';
import CommandePayment from './components/CommandePayment.vue';
import balance from './components/balance.vue';
import livre from './components/GeneralLedger.vue';


const routes = [
  {
    path: '/',
    redirect: '/login', // uniquement redirection
  },

{
    path: '/livre',
    name: 'livre',
    component: livre,
    meta: { requiresAuth: true }
  },
{
    path: '/balance',
    name: 'balance',
    component: balance,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/commande&payment',
    name: 'commande&payment',
    component: CommandePayment,
    meta: { requiresAuth: true }
  },
    { path: '/journals',
      name: 'Journals',
      component: JournalManager,
     meta: { requiresAuth: true }
     },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },


  {
    path: "/partners",
    name: "Partners",
    component: Partners,
    meta: { requiresAuth: true }

  },
  {
    path: '/partners-list',
    name: 'PartnerList',
    component: PartnerList,
    meta: { requiresAuth: true },
  },
  {
    path: '/comptes',
    name: 'Comptes',
    component: Comptes,
    meta: { requiresAuth: true } // accessible seulement si connecté
  },
  // autres routes protégées
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

function isLoggedIn() {
  const token = localStorage.getItem('access_token')
  if (!token) return false

  try {
    const payload = JSON.parse(atob(token.split('.')[1])) // décoder le JWT
    const expiry = payload.exp * 1000 // en ms
    return Date.now() < expiry // true si encore valide
  } catch (e) {
    return false
  }
}


router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !isLoggedIn()) {
    next({ name: 'Login' })
  } else if (to.name === 'Login' && isLoggedIn()) {
    next({ name: 'Dashboard' })
  } else {
    next()
  }
})

export default router
