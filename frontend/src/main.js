import Vue from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios';
import ElementUI from 'element-ui';
import locale from 'element-ui/lib/locale/lang/en'
import VueI18n from 'vue-i18n';
import {
    messages
} from './components/common/i18n';
// import 'element-ui/lib/theme-chalk/index.css'; // 默认主题
// import './assets/css/theme-green/index.css';       // 浅绿色主题
import './assets/css/icon.css';
import './components/common/directives';
import "babel-polyfill";
//顶部页面加载条
import NProgress from 'nprogress';
import 'nprogress/nprogress.css';

import store from './store'
// 自定义组件
import vuePlugin from './vuePlugin'
Vue.use(vuePlugin)
import htmlToPdf from './/vuePlugin/htmlToPdf'
// 使用Vue.use()方法就会调用工具方法中的install方法
Vue.use(htmlToPdf)

////import Mock from './mock/mock'
Vue.config.productionTip = false
Vue.use(VueI18n);
Vue.use(ElementUI, {
    locale,
    size: 'small'
});
const i18n = new VueI18n({
    locale: 'en',
    messages
});
Vue.prototype.$axios = axios;
//Mock.bootstrap();
NProgress.configure({
    easing: 'ease',
    speed: 500,
    showSpinner: false,
    trickleSpeed: 200,
    minimum: 0.3
})
// 使用钩子函数对路由缓存清楚
router.beforeEach((to, from, next) => {
    // if (from.path == '/sampleDetails')  {
    // if (to.path == '/search') {
    //     to.meta.keepAlive = true  //修改为 true
    // }
    // }
    // NProgress.start();
    if (to.path === from.path && JSON.stringify(to.query) === JSON.stringify(from.query)) {
        // 如果是重复导航，不进行任何操作
        return;
    }
    next();
})

//顶部页面加载条

//路由跳转结束
router.afterEach((to, from, next) => {
    if (from.path == '/sampleDetails' || from.path == '/integrationDetails') {
        NProgress.done()
    }
})



new Vue({
    router,
    store,
    i18n,
    render: h => h(App)
}).$mount('#app')