module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  devServer: {
    proxy: {
      '/wf': {
        target: 'http://192.168.100.147:5000/',
        pathRewrite: {'^/wf' : ''}
      }
    }
  },
  css: {
    loaderOptions: {
      scss: {
        additionalData: `
          $VUE_APP_RESOURCE_URL: '${process.env.VUE_APP_RESOURCE_URL}';
        `
      }
    }
  }
}
