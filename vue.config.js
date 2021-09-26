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
  }
}
