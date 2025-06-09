module.exports = {

    publicPath: process.env.NODE_ENV === 'production' ? '/' : '/',
    // publicPath: process.env.NODE_ENV === "production" ? "/ipscdb/" : "/",
    // assetsDir: './ipscdb',
    productionSourceMap: false,
    devServer: {
        //port:8888,
        proxy: {
            '/api': {
                target: 'http://jsonplaceholder.typicode.com',
                changeOrigin: true,
                pathRewrite: {
                    '/api': ''
                }
            },
            '/testApi': {
                target: 'http://111.8.20.247:89/api/apph5api',
                changeOrigin: true,
                pathRewrite: {
                    '^/testApi': '/testApi'
                }
            },
            '/ms': {
                target: 'https://www.easy-mock.com/mock/592501a391470c0ac1fab128',
                changeOrigin: true
            }
        }
    }
}