import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify' 
import { createPinia } from 'pinia'
import CustomTitle from './components/global/CustomTitle.vue'

const app = createApp(App)
app.component('custom-title', CustomTitle)

app.use(router)
app.use(createPinia())
app.use(vuetify)
app.mount('#app')
