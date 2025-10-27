/**
 * 旅行相关API
 */
import request from './request'

/**
 * 获取旅行列表
 * @param {Object} params - 查询参数
 */
export const getTripList = (params) => {
    return request.get('/trips/', { params })
}

/**
 * 获取旅行详情
 * @param {string} slug - 旅行标识符
 */
export const getTripDetail = (slug) => {
    return request.get(`/trips/${slug}/`)
}

/**
 * 点赞旅行
 * @param {string} slug - 旅行标识符
 */
export const likeTrip = (slug) => {
    return request.post(`/trips/${slug}/like/`)
}

/**
 * 打卡旅行
 * @param {string} slug - 旅行标识符
 */
export const checkinTrip = (slug) => {
    return request.post(`/trips/${slug}/checkin/`)
}

/**
 * 获取旅行统计
 * @param {string} slug - 旅行标识符
 */
export const getTripStats = (slug) => {
    return request.get(`/trips/${slug}/stats/`)
}

/**
 * 获取旅行评论
 * @param {string} slug - 旅行标识符
 * @param {Object} params - 查询参数
 */
export const getTripComments = (slug, params) => {
    return request.get(`/trips/${slug}/comments/`, { params })
}

