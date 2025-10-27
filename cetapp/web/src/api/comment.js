/**
 * 评论相关API
 */
import request from './request'

/**
 * 获取评论列表
 * @param {Object} params - 查询参数 {trip, page_size, user}
 * @param {string} params.trip - 旅行页面标识（必需）
 * @param {number} params.page_size - 每页数量
 * @param {number} params.user - 用户ID过滤
 */
export const getCommentList = (params) => {
    return request.get('/comments/', { params })
}

/**
 * 创建评论
 * @param {FormData} data - 表单数据（包含文件）
 */
export const createComment = (data) => {
    return request.post('/comments/', data, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
}

/**
 * 删除评论
 * @param {number} id - 评论ID
 */
export const deleteComment = (id) => {
    return request.delete(`/comments/${id}/`)
}

/**
 * 获取评论详情
 * @param {number} id - 评论ID
 */
export const getCommentDetail = (id) => {
    return request.get(`/comments/${id}/`)
}

