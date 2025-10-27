/**
 * API配置
 * 
 * 开发环境：通过 vue.config.js 代理访问后端（/api, /static, /media）
 * 生产环境：
 *   - 如果前后端同域：直接使用相对路径
 *   - 如果前后端分离：配置 VUE_APP_API_BASE_URL 环境变量
 */

// 根据环境获取API基础URL
export const getApiBaseUrl = () => {
    // 使用环境变量（生产环境配置）
    // 如果未配置，返回空字符串（使用相对路径）
    return process.env.VUE_APP_API_BASE_URL || ''
}

// 获取完整URL（处理相对路径）
export const getFullUrl = (path) => {
    if (!path) return null

    // 如果已经是完整URL，直接返回
    if (path.startsWith('http://') || path.startsWith('https://')) {
        return path
    }

    // 获取API基础URL
    const baseUrl = getApiBaseUrl()

    // 如果baseUrl为空，直接返回相对路径（开发环境通过代理，生产环境同域）
    if (!baseUrl) {
        return path
    }

    // 拼接完整URL（生产环境跨域）
    return baseUrl + path
}

// 获取头像URL
export const getAvatarUrl = (avatarUrl) => {
    if (!avatarUrl) {
        return getFullUrl('/static/images/default_avatar.png')
    }
    return getFullUrl(avatarUrl)
}

export default {
    getApiBaseUrl,
    getFullUrl,
    getAvatarUrl
}

