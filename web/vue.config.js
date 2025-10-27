const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,

  // 开发服务器配置
  devServer: {
    port: 8080,
    proxy: {
      // 代理API请求
      '^/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        ws: true,
      },
      // 代理静态文件（头像等）
      '^/static': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      // 代理媒体文件（用户上传的图片、视频）
      '^/media': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      }
    }
  },

  // 生产构建配置
  outputDir: '../static/vue',  // 保持不变，输出到Django的static目录
  assetsDir: 'assets',
  // 部署到Django的static目录
  publicPath: process.env.NODE_ENV === 'production' ? '/static/vue/' : '/'
})
