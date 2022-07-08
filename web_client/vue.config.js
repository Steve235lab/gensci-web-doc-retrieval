const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
    devServer: {

      proxy: {
        '/api': {
          target: 'http://42.192.44.52:8000',
          ws:false,
          changeOrigin: true,
          pathRewrite: {
            '^/api': ''
          }
        }
      }
  }
})
