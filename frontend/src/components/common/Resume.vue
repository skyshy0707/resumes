<script lang="ts">
    import { computed, defineComponent, PropType } from 'vue'

    import type Resume from '../structures/annotations'

    export default defineComponent({
        props: {
            resume: Object as PropType<Resume>,
            isDisabled: Boolean
        },
        
        data(){
            return {
                resumeData: this.resume,
                disabled: this.isDisabled
            }
        }
    })
</script>

<template>
    <div>
        <input v-if="resume.id" type="number" name="id" :value="resume.id" hidden/>
        <input type="number" name="user_id" :value="resume.user_id" hidden/>
        <input type="text" name="title" :disabled="isDisabled" required v-model="resume.title" />
        <textarea name="content" :disabled="isDisabled" @update:disabled="disabled = $event"  v-model="resume.content"><slot></slot></textarea>
    </div>
</template>