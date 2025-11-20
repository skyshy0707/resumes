<template>

    <form @submit="registration">
        <p>Registration</p>
        <Credentials :credentials="credentials" class="flex flex-col gap-4 w-full sm:w-64">
         
        </Credentials>
    </form>
    
</template>

<script>
import axios from "axios"
import Credentials from '../common/Credentials.vue'



export default {
    name: 'Registration',
    components: {
        Credentials
    },

    data(){
        return {
            credentials: {
                password: ''
            }
        }
    },

    methods: {

        async registration(event) {
            event.preventDefault()
            axios.defaults.headers.common["Authorization"] = `Basic ${btoa(this.credentials.username + ':' + this.credentials.password)}`
            axios.post(
                `${this.$store.state.SERVER_BASE_URL}/registration`,
                { 
                    headers: { 
                        'Accept': 'application/json',
                        'Authorization': `Basic ${btoa(this.credentials.username + ':' + this.credentials.password)}`
                    },
                    withCredentials: true
                }
            ).then(
                (response) => {
                    console.log(`Response: ${Object.keys(response)}`)
                    this.$router.push('/signup')
                }
            ).catch(
                (error) => {
                    console.log(`Error occur: ${error}. Code: ${error.code}, Obj: ${Object.keys(error)}, Request: ${Object.keys(error.request)}, Config: ${Object.keys(error.config)}, Config.url: ${error.config.url}, message: ${error.message}, name: ${error.name}, request: ${Object.keys(error.request)}`)
                }
            )
        }
}   

}
</script>
