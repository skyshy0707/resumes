import express from 'express';
import { renderToString } from '@vue/server-renderer'

//import app from './client-entry.js'

import { application } from './main.js'


async function render(pageData){
    const { app, router, store } = application()
    router.push(pageData)
    await router.isReady()
    const renderedHTML = await renderToString(app)
    const state = `<script>window.__INITIAL_STATE=${JSON.stringify(store.state)}`

    return `<div id="app">${renderedHTML}</div>${state}`
}

const server = express()


server.get('*', (request, response) => {

    const pageData = { url: request.url }
    
    render(pageData).then(({ html, css }) => {
        response.send(
            `
                <!DOCTYPE html>
                <html lang="en">
                    <head>
                        <title></title>
                        <style></style>
                    </head>
                    <body>
                        ${html}
                    </body>
                </html>
            `
        )
    })
})

server.listen(82, () => {
    console.log("Server was ran on 82th port")
})