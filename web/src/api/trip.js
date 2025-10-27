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
 * 先尝试从新Trip模型获取，失败则尝试旧SiteStat
 */
export const getTripDetail = async (slug) => {
    // 先尝试新的Trip模型
    try {
        return await request.get(`/trip-plans/${slug}/`)
    } catch (error) {
        // 如果失败（404），尝试旧的SiteStat
        if (error.response?.status === 404) {
            return await request.get(`/trips/${slug}/`)
        }
        throw error
    }
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

