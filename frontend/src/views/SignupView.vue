<!-- src/views/SignupView.vue -->
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const form   = ref({
  username: '',
  password: '',
  email:    '',
  latitude: 0,
  longitude:0
})
const msg = ref('')

async function signup() {
  try {
    await axios.post('/api/signup', form.value)
    // success → go to pending screen
    router.push('/pending')
  } catch (e) {
    msg.value = e.response?.data?.error || 'Signup failed'
  }
}
</script>

<template>
  <div class="max-w-md mx-auto p-6">
    <h1 class="text-2xl font-bold mb-4">Farmer Sign‑up</h1>

    <form @submit.prevent="signup" class="space-y-2">
      <input v-model="form.username"  placeholder="Username" class="border p-2 w-full" />
      <input v-model="form.password"  type="password" placeholder="Password" class="border p-2 w-full" />
      <input v-model="form.email"     type="email" placeholder="Email" class="border p-2 w-full" />
      <div class="flex space-x-2">
        <input v-model.number="form.latitude"  placeholder="Lat" class="border p-2 w-1/2" />
        <input v-model.number="form.longitude" placeholder="Lng" class="border p-2 w-1/2" />
      </div>
      <button class="bg-green-600 text-white px-4 py-2 w-full">Sign up</button>
    </form>

    <p class="mt-3 text-center text-red-600">{{ msg }}</p>
  </div>
</template>

