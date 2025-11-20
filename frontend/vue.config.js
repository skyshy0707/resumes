/*import { defineConfig } from '@vue/cli-service'*/

//const { defineConfig } = require('@vue/cli-service')
const NodePolyfillPlugin = require("node-polyfill-webpack-plugin")

module.exports = {
    runtimeCompiler: true,
    transpileDependencies: true,
    chainWebpack: config => {
        config.plugin('polyfills').use(NodePolyfillPlugin)
        //config.resolve.alias.set('vue', '@vue/compat')
    },
    configureWebpack: {
        plugins: [new NodePolyfillPlugin()],
        optimization: {
            splitChunks: {
                chunks: "all",
            },
        },
    }
}


//module.exports = config