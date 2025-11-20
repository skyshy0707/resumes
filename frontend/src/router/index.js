import { createMemoryHistory, createWebHistory, createRouter } from 'vue-router'

import Profile from '../components/pages/Profile.vue'
import Registration from '../components/pages/Registration.vue'
import Signup from '../components/pages/Signup.vue'


const routes = [
  { path: '/', component: Profile, name: 'Profile' },
  { path: '/registration', component: Registration, props: true, name: 'Registration' },
  { path: '/signup', component: Signup, props: true, name: 'Signup' }
]

const router = createRouter({ 
  routes,
  history: createWebHistory(),
   
})

const nonAuthEndpoints = [
  'Registration', 'Signup'
]


router.beforeEach(async (to, from, next) => {
  const authToken = await cookieStore.get('auth-token')
  console.log(`authToken: ${authToken}`)
  if (authToken || nonAuthEndpoints.includes(to.name)){
    next()
  }
  else next({ name: 'Signup' })
})

export default router