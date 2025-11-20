class Email extends String{
    constructor (value){
        super()
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)){
            throw new Error(`Invalid email format value: ${value}`)
        }
        this.value = value
    }
}



export default Email