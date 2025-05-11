<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const products = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const res = await axios.get('/api/products')
    products.value = res.data
  } catch (err) {
    error.value = 'Failed to load products'
    console.error(err)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">Product List</h1>

    <div v-if="loading">Loading...</div>
    <div v-if="error" class="text-red-600">{{ error }}</div>

    <div v-if="!loading && products.length === 0">No products found.</div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
      <div v-for="product in products" :key="product.id" class="border p-4 rounded shadow">
        <h2 class="text-xl font-semibold">{{ product.name }}</h2>
        <p class="text-gray-600">{{ product.description }}</p>
        <p class="mt-2 font-bold">£{{ product.price.toFixed(2) }}</p>
        <p class="text-sm text-green-600" v-if="product.available">Available</p>
        <p class="text-sm text-red-600" v-else>Out of stock</p>
      </div>
    </div>
  </div>
</template>

