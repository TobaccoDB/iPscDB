import Vue from 'vue'
import axios from '../api/http.js';

const vuePlugin = () => {
    Vue.mixin({
        data() {
            return {}
        },
        created() {},
        methods: {
            jg_downloadFile(url, param) {
                let newUrl = `${axios.defaults.baseURL}${url}?`
                // if (axios.defaults.baseURL == 'http://plncdb.tobaccodb.org/server_pcmdb/') {
                //     newUrl = `${axios.defaults.baseURL}${url}?`
                // } else {
                //     newUrl = `${axios.defaults.baseURL}/${url}?`
                // }
                Object.keys(param).forEach((key) => {
                    newUrl += `${key}=${param[key]}&`
                })
                const link = document.createElement('a') // 创建a标签    
                link.target = '_blank' // a标签添加属性    
                link.href = newUrl.substring(0, newUrl.length - 1)
                link.style.display = 'none'
                document.body.appendChild(link)
                link.click() // 执行下载     
                document.body.removeChild(link)
            }
        }
    })
}

export default vuePlugin