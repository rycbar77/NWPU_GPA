import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui'
import router from './router'
import 'element-ui/lib/theme-chalk/index.css'
import store from './store'
import qs from 'qs'

Vue.prototype.$qs = qs
var axios = require('axios')
axios.defaults.baseURL = 'http://localhost:5000'
axios.defaults.headers['Content-Type'] = 'application/x-www-form-urlencoded';
Vue.prototype.$axios = axios
Vue.config.productionTip = false
Vue.use(ElementUI)
router.beforeEach((to, from, next) => {
        if (to.meta.title) {
            document.title = to.meta.title
        }
        if (to.fullPath === '/') {
            next({
                path: 'login'
            })
        } else {
            if (to.meta.requireAuth) {
                if (store.state.user.username) {
                    next()
                } else {
                    next({
                        path: 'login',
                        query: {redirect: to.fullPath}
                    })
                }
            } else {
                next()
            }
        }
    }
)

new Vue({
    render: h => h(App),
    router,
    store,
}).$mount('#app')
