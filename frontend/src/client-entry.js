//import { app, router, store } from './main.js'
import application from './main.js'

const { app, router, store } = application()

const storeInitialState = window.INITIAL_DATA

if (storeInitialState){
    store.replaceState(storeInitialState)
}

/*router.isReady().then(() => {
    console.log("It Is ready")
    app.mount('#app')
})*/

app.mount('#app')