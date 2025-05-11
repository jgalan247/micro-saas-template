<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
const auth = useAuthStore()
</script>

<template>
  <nav class="p-4 bg-gray-100 space-x-2">
    <RouterLink to="/products">Products</RouterLink>
    <RouterLink to="/map">Map</RouterLink>
    <RouterLink v-if="!auth.isLogged" to="/login">Login</RouterLink>
    <RouterLink v-if="!auth.isLogged" to="/signup">Sign‑up</RouterLink>
    <RouterLink v-if="auth.isLogged" to="/admin">Admin</RouterLink>
    <button
      v-if="auth.isLogged"
      @click="auth.logout()"
      class="text-blue-600 underline"
    >
      Logout ({{ auth.user.username }})
    </button>
  </nav>

  <RouterView />
</template>

