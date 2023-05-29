import store from "@/store";
import { createRouter,createWebHistory} from 'vue-router';


const router = createRouter({
  history: createWebHistory(),
  routes: [
     {
        path: '/',
        name: 'login',
        component: () => import('@/components/login.vue'),
        meta: {
          requiresAuth: false
        }
     },
     {
        path: '/signup',
        name: 'signup',
        component: () => import('@/components/signup.vue'),
        meta: {
          requiresAuth: false
        }
      },
           {
        path: '/shipping',
        name: 'shipping',
        component: () => import('@/components/shipmentsList.vue'),
        meta: {
          requiresAuth: true
        }
      },

 ]
})

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (!store.getters.getToken) {
            next({name: 'login'})
        } else {
            next()
        }
    } else {
        next()
    }
    }
)

export default router;