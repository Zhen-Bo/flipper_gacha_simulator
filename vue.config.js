module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  chainWebpack: (config) => {
    if (process.env.NODE_ENV === 'production') {
      config.plugin('html').tap((opts) => {
        opts[0].filename = '../templates/index.html';
        return opts;
      });

    }
  },
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
