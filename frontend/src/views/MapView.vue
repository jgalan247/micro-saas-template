<!-- src/views/MapView.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { LMap, LTileLayer, LMarker, LPopup } from '@vue-leaflet/vue-leaflet'

/* ── reactive state ───────────────────────────── */
const locations = ref([])
const productsByLoc = ref({})   // { 1: [ {...}, {...} ], 2: [...] }

/* ── fetch data once ──────────────────────────── */
onMounted(async () => {
  const [locRes, prodRes] = await Promise.all([
    axios.get('/api/locations'),
    axios.get('/api/products'),
  ])

  locations.value = locRes.data

  // group products by location_id
  const map = {}
  for (const p of prodRes.data) {
    if (!map[p.location_id]) map[p.location_id] = []
    map[p.location_id].push(p)
  }
  productsByLoc.value = map
})
</script>

<template>
  <h1 class="text-2xl font-bold p-4">Farm Locations</h1>

  <LMap :zoom="11" :center="[49.21, -2.13]" style="height: 70vh; width: 100%">
    <LTileLayer
      url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      attribution="&copy; OpenStreetMap contributors" />

    <LMarker
      v-for="loc in locations"
      :key="loc.id"
      :lat-lng="[loc.latitude, loc.longitude]">
      <LPopup>
        <div class="font-semibold mb-1">{{ loc.name }}</div>

        <ul v-if="productsByLoc[loc.id]?.length">
          <li v-for="p in productsByLoc[loc.id]" :key="p.id">
            • {{ p.name }} — £{{ p.price.toFixed(2) }}
          </li>
        </ul>

        <p v-else class="italic text-gray-500">No products listed</p>
      </LPopup>
    </LMarker>
  </LMap>
</template>

