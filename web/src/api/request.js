/**
 * 基于fetch的Ajax请求封装
 */
const baseURL = process.env.VUE_APP_API_BASE_URL || '/api/v1'

// 创建request函数，模拟axios接口
const request = {
    // GET请求
    async get(url, config = {}) {
        // 处理query参数
        const { params, ...options } = config
        let finalUrl = url
        if (params && Object.keys(params).length > 0) {
            const queryString = new URLSearchParams(params).toString()
            finalUrl = `${url}?${queryString}`
        }
        return this.request(finalUrl, {
            method: 'GET',
            ...options
        })
    },

    // POST请求
    async post(url, data, config = {}) {
        return this.request(url, {
            method: 'POST',
            body: data instanceof FormData ? data : JSON.stringify(data),
            ...config
        })
    },

    // PUT请求
    async put(url, data, config = {}) {
        return this.request(url, {
            method: 'PUT',
            body: data instanceof FormData ? data : JSON.stringify(data),
            ...config
        })
    },

    // PATCH请求
    async patch(url, data, config = {}) {
        return this.request(url, {
            method: 'PATCH',
            body: data instanceof FormData ? data : JSON.stringify(data),
            ...config
        })
    },

    // DELETE请求
    async delete(url, config = {}) {
        return this.request(url, {
            method: 'DELETE',
            ...config
        })
    },

    // 通用请求方法
    async request(url, options = {}) {
        // 构建完整URL
        const fullUrl = url.startsWith('http') ? url : `${baseURL}${url}`

        // 构建headers
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        }

        // 从localStorage获取token
        const token = localStorage.getItem('access_token')
        if (token) {
            headers.Authorization = `Bearer ${token}`
        }

        // 处理FormData，移除Content-Type让浏览器自动设置
        if (options.body instanceof FormData) {
            delete headers['Content-Type']
        }

        // 构建请求选项
        const fetchOptions = {
            ...options,
            headers,
            credentials: 'same-origin'
        }

        // 发送请求
        const response = await fetch(fullUrl, fetchOptions)

        // 检查响应状态
        if (!response.ok) {
            const error = new Error(`Request failed with status ${response.status}`)
            error.response = response
            error.status = response.status
            error.statusText = response.statusText

            try {
                const errorData = await response.json()
                console.log('[API Error]', url, errorData)
                error.message = errorData.detail || errorData.message || error.message
                error.response.data = errorData
            } catch (e) {
                console.log('[API Error]', url, 'Failed to parse error response')
                error.message = response.statusText || error.message
            }

            // 处理401未授权
            if (response.status === 401) {
                // 清掉本地失效令牌（避免公共页携带坏token导致跳转）
                localStorage.removeItem('access_token')
                localStorage.removeItem('refresh_token')
                localStorage.removeItem('user_info')

                // 仅在需要登录的路由上跳转登录，其余公共页不跳转
                const path = window.location.pathname || ''
                const needAuth = path.startsWith('/user') || path.startsWith('/editor') || path.startsWith('/my-trips')
                if (needAuth && path !== '/login/' && path !== '/login') {
                    window.location.href = '/login/'
                }
            }

            throw error
        }

        // 检查响应是否有内容（204 No Content没有响应体）
        if (response.status === 204 || response.headers.get('content-length') === '0') {
            return null
        }

        // 解析响应数据
        const data = await response.json()
        return data
    }
}

export default request

