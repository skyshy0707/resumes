<template>

    
    <div>
        <div>
            <input type="text" name="content" v-model="searchResumeParams.content" placeholder="&#x1F50D; content"/>
            <input type="text" name="title" v-model="searchResumeParams.title" placeholder="&#x1F50D; title"/>
            <button @click="searchResumes()">Search</button>
            <button @click="resetSearchResumes()">Reset</button>
        </div>
        <ul>
            <li v-for="resumeItem in resumes" :key="resumeItem.id">
                {{ resumeItem.title }} 
                <a v-bind:href="$store.state.SERVER_BASE_URL + '/resume' + resumeItem.id + '/view'" role="button" @click="getResume">View</a>
            </li> 
            <div @click="paginate($event, totalResumes)">
                <button>first</button>
                <button><</button>
                <button>></button>
                <button>last</button>
            </div>

        </ul>

       <form v-on:submit="editResume">
            <div v-if="resumeFormIsVisible">

                <Resume :resume="resume" :isDisabled="!editResumeVisible">
                </Resume>

                <div>
                    <button @click="switchEditResumeForm()" type="button">Edit</button>
                    <button type="submit" v-if="editResumeVisible">Apply</button>
                    <button @click="deleteResume()" type="button">Delete</button>
                </div>
            </div>
        </form> 

        <form v-on:submit="createResume">
            <button @click="switchCreateResumeForm()" type="button">+</button>

            <div v-if="createResumeVisible">
                <Resume :resume="newResume" :isDisabled="!createResumeVisible">

                </Resume>
                <div>
                    <button type="submit">Create</button>
                </div>
            </div>

        </form>

        <p>State: {{ message }}</p>


        <span :text="messageResumeState"> {{ messageResumeState }}</span>
    </div>
</template>

<script>
import axios from "axios"

axios.defaults.headers.get['Accepts'] = 'application/json';
axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';
axios.defaults.headers.common['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept';

import Resume from '../common/Resume.vue'
import resume from '../structures/profile.js'


export default {
    name: 'Profile',
    components: {
        Resume
    },

    data(){
        return {
            resumeFormIsVisible: false,
            editResumeVisible: false,
            createResumeVisible: false,
            messageResumeState: null,
            resumes: [],
            resume: resume,
            newResume: resume,
            message: '',
            currentOffset: 0,
            offsetStep: 10,
            totalResumes: 0,
            searchResumeParams: {
                content: '',
                title: ''
            }
        }
    },
    methods: {

        async paginate(event, total){
            event.preventDefault()
            console.log(`target text: ${event.target.innerText}`)
            let paginateWay = event.target.innerText

            if (paginateWay == '>' && (this.currentOffset + this.offsetStep) < total ){
                this.currentOffset += this.offsetStep
            }
            else if (paginateWay =='<' && this.currentOffset > 0){
                this.currentOffset -= this.offsetStep
            }
            else if (paginateWay == 'last'){
                this.currentOffset = total > (this.currentOffset + this.offsetStep) ? 
                    Math.floor(total/this.offsetStep) * this.offsetStep : this.currentOffset
            }
            else if (paginateWay == 'first'){
                this.currentOffset = 0
            }
            
            console.log(`current offset ${this.currentOffset}`)
            this.resumes = await this.getUserResumes(this.currentOffset)
        },


        async searchResumes(){
            this.resumes = await this.getUserResumes()
        },

        resetSearchResumes(){
            for (let key of Object.keys(this.searchResumeParams)){
                this.searchResumeParams[key] = ''
            }
        },
        
        switchCreateResumeForm(){
            this.createResumeVisible = !this.createResumeVisible
        }
        ,
        switchEditResumeForm(){
            this.editResumeVisible = !this.editResumeVisible
        },

        getAuthToken(){
            return this.$cookies.get("auth-token")
        }, 

        setAuthTokenToCommonHeaders(){
            let authToken = this.getAuthToken()
            axios.defaults.headers.common["Authorization"] = `Bearer ${authToken}`
        },

        async getUserResumes(offset=0){

            console.log(`in c-headers - Authorization: ${axios.defaults.headers.common["Authorization"]}`)
            let response
            console.log(`${this.$store.state.SERVER_BASE_URL}/resumes`)
            try{
                response = await axios.get(
                    `${this.$store.state.SERVER_BASE_URL}/resumes`,
                    {
                        headers: {
                            Authorization: this.getAuthToken()
                        },
                        params: {
                            offset: offset,
                            ...this.searchResumeParams
                        },
                        withCredentials: true
                    }
                )

                this.totalResumes = response.data.total
            }
            catch(error){
                console.log(`Keys: ${Object.keys(error)}`)
                let errorData = JSON.stringify(error.response.data)
                console.log(`Detail: ${errorData}`)
            }

            return response ? response.data.items : {}
        },

        /*click handler*/
        getResume(event){
            event.preventDefault()
            let resumeUrl = event.target

            console.log(`Resume url: ${resumeUrl}`)
            axios.get(
                resumeUrl,
                {
                    headers: {
                        Authorization: this.getAuthToken()
                    },
                    withCredentials: true
                }
            )
            .then(
                (response) => {
                    this.resume = response.data
                    this.resumeFormIsVisible = true
                }
            ).catch(
                (error) => {console.log(`Error occur: ${error}`)}
            )
        },
        createResume(event){
            event.preventDefault()
            var createResumeUrl = `${this.$store.state.SERVER_BASE_URL}/resume/create`
            this.newResume.user_id = this.$cookies.get("user_id")
            axios.post(
                createResumeUrl,
                this.newResume,
                {
                    withCredentials: true
                }
            ).then(
                (response) => {
                    this.message = `A new resume with id=${response.data.id} was created`
                    console.log(this.message)
                    this.newResume.title = ''
                    this.newResume.content = ''

                }
            ).catch(
                (error) => { 
                    let errorData = JSON.stringify(error.response.data)
                    console.log(`Detail: ${errorData}`)
                }
            )
        },
        editResume(event){
            event.preventDefault()
            var id = this.resume.id
            var editResumeUrl = `${this.$store.state.SERVER_BASE_URL}/resume${id}/edit`

            axios.patch(
                editResumeUrl,
                this.resume,
                { 
                    headers: {
                        Authorization: this.getAuthToken()
                    },
                    withCredentials: true
                }
            ).then(
                (response) => {
                    this.resume = response.data
                    this.message = `A resume with id=${response.data.id} was edited`
                }
            ).catch(
                (error) => {console.log(`Error occur: ${error}`)}
            )
        },
        deleteResume(){
            var id = this.resume.id
            var deleteResumeUrl = `${this.$store.state.SERVER_BASE_URL}/resume${id}/delete`
            axios.delete(
                deleteResumeUrl,
                { 
                    headers: {
                        Authorization: this.getAuthToken()
                    },
                    withCredentials: true
                }
            ).then(
                (response) => {
                    let id = response.data.id
                    this.resumeFormIsVisible = false
                    this.messageResumeState = `Resume with id=${id} was deleted`
                }
            ).catch(
                (error) => {console.log(`Error occur: ${error}`)}
            )
        }
    },
    created(){
        this.setAuthTokenToCommonHeaders()
    },
    async mounted() {
        this.resumes = await this.getUserResumes()
    },
}

</script>
