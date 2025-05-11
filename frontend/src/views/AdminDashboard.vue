<!-- src/views/AdminDashboard.vue -->
<script setup>
/* ─────────────────────────── Imports ─────────────────────────── */
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'

/* ─────────────────────────── State ───────────────────────────── */
const auth      = useAuthStore()

// product management
const products  = ref([])
const newProd   = ref({
  name: '', description: '', price: 0, location_id: 1, available: true
})

// pending farmer confirmation (visible only to super admin)
const pending   = ref([])

/* ─────────────────────────── API helpers ─────────────────────── */
async function fetchProducts() {
  const { data } = await axios.get('/api/products')
  products.value = data
}

async function addProduct() {
  await axios.post('/api/products', newProd.value)
  newProd.value = { name:'', description:'', price:0, location_id:1, available:true }
  await fetchProducts()
}

async function deleteProduct(id) {
  await axios.delete(`/api/products/${id}`)
  await fetchProducts()
}

async function fetchPending() {
  if (!auth.isSuper) return
  const { data } = await axios.get('/api/users/unconfirmed')
  pending.value = data
}

async function confirmFarmer(id) {
  await axios.put(`/api/users/confirm/${id}`)
  await fetchPending()
}

/* ─────────────────────────── Lifecycle ──────────────────────── */
onMounted(async () => {
  await fetchProducts()
  await fetchPending()
})
</script>

<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">Admin Dashboard</h1>

    <!-- ── Add‑product form ─────────────────────────────────── -->
    <div class="border p-4 mb-6 max-w-md">
      <h2 class="font-semibold mb-2">Add Product</h2>
      <input v-model="newProd.name"         placeholder="Name"        class="border p-1 mb-1 w-full" />
      <input v-model="newProd.description"  placeholder="Description" class="border p-1 mb-1 w-full" />
      <input v-model.number="newProd.price" type="number" min="0" step="0.01"
             placeholder="Price"            class="border p-1 mb-1 w-full" />
      <button @click="addProduct" class="bg-green-600 text-white px-3 py-1 mt-1">Add</button>
    </div>

    <!-- ── Product table ─────────────────────────────────────── -->
    <table class="w-full text-left border">
      <thead>
        <tr class="bg-gray-100">
          <th class="px-2 py-1">Name</th>
          <th class="px-2 py-1">Price (£)</th>
          <th class="px-2 py-1">Available</th>
          <th class="px-2 py-1"></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="p in products" :key="p.id" class="border-t">
          <td class="px-2 py-1">{{ p.name }}</td>
          <td class="px-2 py-1">{{ p.price.toFixed(2) }}</td>
          <td class="px-2 py-1">
            <span :class="p.available ? 'text-green-600' : 'text-red-600'">
              {{ p.available ? 'Yes' : 'No' }}
            </span>
          </td>
          <td class="px-2 py-1">
            <button @click="deleteProduct(p.id)" class="text-red-600">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- ── Pending farmers (super‑admin only) ────────────────── -->
    <div v-if="auth.isSuper" class="mt-10">
      <h2 class="text-xl font-bold mb-2">Pending Farmer Approvals</h2>
      <div v-if="pending.length === 0" class="text-gray-500">None pending.</div>
      <ul>
        <li v-for="u in pending" :key="u.id" class="flex justify-between border-b py-1">
          <span>{{ u.username }} ({{ u.email }})</span>
          <button @click="confirmFarmer(u.id)" class="text-green-600">Approve</button>
        </li>
      </ul>
    </div>
  </div>
</template>

