import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import axios from 'axios'
import VueAxios from 'vue-axios'
Vue.prototype.$axios = axios
Vue.use(VueAxios, axios) 
Vue.use(ElementUI);
Vue.config.productionTip = false

new Vue({
  axios,
  router,
  store,
  render: h => h(App)
}).$mount('#app')
axios.default.baseURL='/test'