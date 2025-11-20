import Vuex from 'vuex'


const store = Vuex.createStore({
    state() {
        return { 
            SERVER_BASE_URL: 'http://localhost:9006/api' 
        }
    }
})

export default store