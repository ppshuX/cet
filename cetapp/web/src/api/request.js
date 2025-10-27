/**
 * Axios请求封装
 */
import axios from 'axios'

// 创建axios实例
const request = axios.create({
    baseURL: process.env.VUE_APP_API_BASE_URL || '/api/v1',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json'
    }
})

// 请求拦截器
request.interceptors.request.use(
    config => {
        // 从localStorage获取token
        const token = localStorage.getItem('access_token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    error => {
        console.error('请求错误:', error)
        return Promise.reject(error)
    }
)

// 响应拦截器
request.interceptors.response.use(
    response => {
        return response.data
    },
    error => {
        console.error('响应错误:', error)

        // 处理401未授权
        if (error.response && error.response.status === 401) {
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token')
            localStorage.removeItem('user_info')

            // 跳转到登录页
            if (window.location.pathname !== '/login') {
                window.location.href = '/#/login'
            }
        }

        // 提取错误消息
        const message = error.response?.data?.detail ||
            error.response?.data?.message ||
            error.message ||
            '请求失败'

        return Promise.reject(new Error(message))
    }
)

export default request

