import Credentials from '../common/Credentials.vue'
import Resume from '../common/Resume.vue'
import Email from './types.js'

interface Credentials{
    username: Email
    password: String
}

interface Resume{
    id?: Number
    user_id: Number
    title?: String
    content?: Text
}

export default Credentials; Resume