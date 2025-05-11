<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const auth   = useAuthStore()
const creds  = ref({ username:'', password:'' })
const error  = ref('')

async function login() {
  try {
    await auth.login(creds.value.username, creds.value.password)
    // redirect based on confirmation
    if (auth.isConfirmed) router.push('/admin')
    else                  router.push('/pending')
  } catch {
    error.value = 'Login failed. Check credentials.'
  }
}
</script>

<template>
  <div class="max-w-xs mx-auto p-6">
    <h1 class="text-2xl font-bold mb-4">Login</h1>
    <form @submit.prevent="login" class="space-y-2">
      <input v-model="creds.username" placeholder="Username" class="border p-2 w-full" />
      <input v-model="creds.password" type="password" placeholder="Password" class="border p-2 w-full" />
      <button class="bg-blue-600 text-white px-4 py-2 w-full">Login</button>
    </form>
    <p class="mt-3 text-center text-red-600">{{ error }}</p>
  </div>
</template>

