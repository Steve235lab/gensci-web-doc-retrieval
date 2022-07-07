const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  //vue.config.js
    devServer: {
      // host: 'localhost',
      // port: 8080,//本地运行的端口
      //接口代理
      proxy: {
        '/api': {
          target: 'http://42.192.44.52:8000',//设置要代理访问的接口
          ws:false,
          changeOrigin: true,
          pathRewrite: {
            '^/api': ''  //重写访问地址，在请求时可以省略target的地址，直接以/api开头
          }
        }
      }
  }
})
