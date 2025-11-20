<template>

    <form @submit="signup">
        <p>Signup</p>
        <Credentials :credentials="credentials" class="flex flex-col gap-4 w-full sm:w-64">
        </Credentials>
    </form>
    
</template>

<script>
import axios from "axios"
import Credentials from '../common/Credentials.vue'


export default {
    name: 'Signup',
    components: {
        Credentials
    },

    data(){
        return {
            credentials: {},
            errorMessage: ''
        }
    },

    methods: {

        async signup(event) {
            event.preventDefault()
            axios.defaults.headers.common["Authorization"] = `Basic ${btoa(this.credentials.username + ':' + this.credentials.password)}`
            axios.put(
                `${this.$store.state.SERVER_BASE_URL}/signup`,
                { 
                    headers: { 
                        'Accept': 'application/json',
                        'Authorization': `Basic ${btoa(this.credentials.username + ':' + this.credentials.password)}`
                    },
                    withCredentials: true
                }
            ).then(
                (response) => {
                    let accessToken = response.data.access_token
                    let userId = response.data.user_id
                    this.$cookies.set('auth-token', accessToken)
                    this.$cookies.set('user_id', userId)
                    this.$router.push('/')
                }
            ).catch(
                (error) => {
                    console.log(`Error occur: ${error}. Detail: ${error.response}, Obj: ${Object.keys(error)}, Response: ${Object.keys(error.response)}, Response.statusText: ${error.response.statusText}, Response.data.detail: ${error.response.data.detail}, Response.headers: ${error.response.headers}, Response.status: ${error.response.status}, message: ${error.message}, Response.data.headers: ${error.response.data.headers}, dir(error.data): ${Object.keys(error.response.data)}`)
                }
            )
        }
}   

}
</script>
