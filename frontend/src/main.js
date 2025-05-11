/* ── Leaflet CSS (must come first for correct icon layout) ── */
import 'leaflet/dist/leaflet.css'

/* ── Axios global base URL ───────────────────────────────── */
import axios from 'axios'
axios.defaults.baseURL = 'http://127.0.0.1:5000'   // Flask API

/* ── Vue core & plugins ──────────────────────────────────── */
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'

/* ── Leaflet core JS (needed by @vue-leaflet) ───────────── */
import * as L from 'leaflet'

/* Fix missing marker icons when Vite bundles assets */
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: new URL('leaflet/dist/images/marker-icon-2x.png', import.meta.url).href,
  iconUrl:       new URL('leaflet/dist/images/marker-icon.png',     import.meta.url).href,
  shadowUrl:     new URL('leaflet/dist/images/marker-shadow.png',   import.meta.url).href,
})

/* ── Create & mount the Vue application ─────────────────── */
const app = createApp(App)
app.use(router)
app.use(createPinia())
app.mount('#app')

