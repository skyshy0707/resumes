<script lang="ts">

import { defineComponent, PropType } from 'vue'

import type Credentials from "../structures/annotations"
import Email from '../structures/types'

export default defineComponent({


    props: {
        credentials: Object as PropType<Credentials>
    },

    data(){
        return {
            dataComponent: this.credentials,
            errorMessage: ''
        }
    },
    methods: {
        validateUsername(){
            let username = this.dataComponent ? this.dataComponent.username : null

            try {
                new Email(username)
                this.errorMessage = ''
            }
            catch {
                this.errorMessage = `Invalid email: ${username}`
            }
        }
    }
})
</script>


<template>
    <div>
        <input name="username" placeholder="username as email:" v-model="dataComponent.username" @input="validateUsername"/>
        <input name="password" placeholder="password:" v-model="dataComponent.password" :feedback="false"/>

        <p v-if="errorMessage">{{ errorMessage }}</p>
        <button type="submit" severity="secondary">Send</button>
    </div>  
</template>

