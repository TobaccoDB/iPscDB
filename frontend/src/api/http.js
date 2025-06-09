import Axios from 'axios' // 此处引入axios官方文件
import {
    Notification
} from 'element-ui'
import qs from 'qs'
import router from '../router'
import store from '../store'

const axios = Axios.create({
    baseURL: process.env.VUE_APP_BASE_URL,
    timeout: 3000000
})

// 添加请求拦截器
axios.interceptors.request.use(
    function (config) {
        if (config.method.toLocaleLowerCase() === 'post' || config.method.toLocaleLowerCase() === 'put') {
            // 参数统一处理，请求都使用data传参
            // config.data = qs.stringify(config.data.data);//序列化post 参数
            config.data = config.data.data //序列化post 参数
        } else if (config.method.toLocaleLowerCase() === 'get' || config.method.toLocaleLowerCase() === 'delete') {
            config.params = config.params
        } else {
            alert('不允许的请求方法：' + config.method)
        }
        return config
    },
    function (error) {
        // 对请求错误做些什么
        return Promise.reject(error)
    }
)

// 添加响应拦截器
axios.interceptors.response.use(
    function (response) {
        // 接口数据处理
        if (response.data === 'Not Found') {
            // 由于不存在的接口有时候会返回Not Found，所以做了特殊处理
            Notification({
                title: response.config.url,
                message: '资源不存在',
                type: 'error'
            })
        } else if (response.status == 200 || response.status == 304) {
            // 自定义约定接口返回{code: xxx, data: xxx, msg:'err message'}
            // code:200 数据正常； ！200 数据获取异常
            if (response.data.code == 200) {
                if (response.config.method.toLocaleLowerCase() === 'post' || response.config.method.toLocaleLowerCase() === 'put') {
                    // Notification({
                    //     title: '成功',
                    //     message: response.data.msg,
                    //     type: 'success'
                    // });
                }
                return response.data
            } else {
                // Notification({
                //     title: response.config.url,
                //     message: response.data.msg,
                //     type: 'error'
                // });
            }
        } else {
            Notification({
                title: response.config.url,
                message: '服务器繁忙，请稍后重试！',
                type: 'error'
            })
        }
    },
    function (error) {
        if (error.response.status == 401) {
            router.push('/')
            return false
        } else if (error.response.status == 403) {
            // Notification({
            //     title: '无权访问',
            //     // message: error.response.data.data.msg,
            //     type: 'info'
            // });
            // router.push('/403');
        } else {
            console.log(error.response.statusText)
            // Notification({
            //     title: '接口异常',
            //     message: error.response.statusText,
            //     type: 'error'
            // });
        }

        return Promise.reject(error)
    }
)
export default axios