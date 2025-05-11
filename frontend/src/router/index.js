import { createRouter, createWebHistory } from 'vue-router'
import ProductListView  from '@/views/ProductListView.vue'
import MapView          from '@/views/MapView.vue'
import LoginView        from '@/views/LoginView.vue'
import AdminDashboard   from '@/views/AdminDashboard.vue'
import PendingView      from '@/views/PendingView.vue'  
import { useAuthStore } from '@/stores/authStore'
import SignupView       from '@/views/SignupView.vue'

const routes = [
  { path: '/products', name: 'Products', component: ProductListView },
  { path: '/map',      name: 'Map',      component: MapView },
  { path: '/login',    name: 'Login',    component: LoginView },
  { path: '/pending',  name: 'Pending',  component: PendingView },
  { path: '/signup',   name: 'Signup',   component: SignupView },
  { path: '/admin',    name: 'Admin',    component: AdminDashboard },
  { path: '/', redirect: '/products' },
]

const router = createRouter({ history: createWebHistory(), routes })

/* Guard /admin */
router.beforeEach((to) => {
  if (to.path === '/admin') {
    const auth = useAuthStore()
    if (!auth.isLogged)     return '/login'
    if (!auth.isConfirmed)  return '/pending'
  }
})

export default router

