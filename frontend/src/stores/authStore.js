import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null                // { id, role, confirmed }
  }),
  getters: {
    isLogged:   s => !!s.user,
    isSuper:    s => s.user?.role === 'super',
    isFarmer:   s => s.user?.role === 'farmer',
    isConfirmed:s => !!s.user?.confirmed,
  },
  actions: {
    async login(username, password) {
      const { data } = await axios.post('/api/login', { username, password })
      this.user = data.user
    },
    logout() { this.user = null }
  }
})

