import Vue from 'vue'
import Router from 'vue-router'
import AppIndex from '../components/home/AppIndex'
import Login from '../components/Login'
// import Home from '../components/Home'

Vue.use(Router)

export default new Router({
    mode: 'history',
    routes: [
        {
            path: '/index',
            name: 'AppIndex',
            component: AppIndex,
            meta: {
                requireAuth: true,
                title: "详情"
            }
        },
        {
            path: '/login',
            name: 'Login',
            component: Login,
            meta:{
                title: "学分绩查询"
            }
        }
    ]
})