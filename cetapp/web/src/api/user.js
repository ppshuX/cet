/**
 * 用户相关API
 */
import request from './request'

/**
 * 获取用户列表
 * @param {Object} params - 查询参数
 */
export const getUserList = (params) => {
    return request.get('/users/', { params })
}

/**
 * 获取用户详情
 * @param {number} id - 用户ID
 */
export const getUserDetail = (id) => {
    return request.get(`/users/${id}/`)
}

/**
 * 更新用户信息
 * @param {number} id - 用户ID
 * @param {Object} data - 更新数据
 */
export const updateUser = (id, data) => {
    return request.patch(`/users/${id}/`, data)
}

// 别名，更语义化
export const updateUserInfo = updateUser

/**
 * 上传头像
 * @param {number} id - 用户ID
 * @param {FormData} data - 头像文件
 */
export const uploadAvatar = (id, data) => {
    return request.post(`/users/${id}/upload_avatar/`, data, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
}

/**
 * 获取用户统计
 * @param {number} id - 用户ID
 */
export const getUserStats = (id) => {
    return request.get(`/users/${id}/stats/`)
}

