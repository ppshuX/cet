/**
 * 认证相关API
 */
import request from './request'

/**
 * 用户注册
 * @param {Object} data - {username, password, password2, email}
 */
export const register = (data) => {
    return request.post('/auth/register/', data)
}

/**
 * 用户登录
 * @param {Object} data - {username, password}
 */
export const login = (data) => {
    return request.post('/auth/login/', data)
}

/**
 * 用户登出
 */
export const logout = () => {
    const refresh = localStorage.getItem('refresh_token')
    return request.post('/auth/logout/', { refresh })
}

/**
 * 获取当前用户信息
 */
export const getCurrentUser = () => {
    return request.get('/auth/me/')
}

/**
 * 刷新Token
 * @param {string} refresh - refresh token
 */
export const refreshToken = (refresh) => {
    return request.post('/token/refresh/', { refresh })
}

