"""
评论相关视图
"""
import os
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from ..models import Comment


@csrf_exempt
@login_required
def add_comment(request):
    """添加评论（trip页面专用）"""
    if not request.user.is_superuser:
        return JsonResponse({'error': '仅管理员可发表评论'}, status=403)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image')
        video = request.FILES.get('video')
        page = request.POST.get('page', 'trip')
        if image:
            ext = os.path.splitext(image.name)[-1]
            image.name = f"{uuid.uuid4().hex}{ext}"
        if video:
            ext = os.path.splitext(video.name)[-1]
            video.name = f"{uuid.uuid4().hex}{ext}"
        if content or image or video:
            Comment.objects.create(content=content, image=image, video=video, user=request.user, page=page)
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'fail', 'message': '只支持POST请求'})


@csrf_exempt
@require_POST
@login_required
def delete_comment(request, comment_id):
    """删除评论（trip页面专用）"""
    try:
        comment = Comment.objects.get(id=comment_id)
        if comment.page != 'trip':
            return JsonResponse({'status': 'forbidden'}, status=403)
        if comment.user == request.user or request.user.is_superuser:
            comment.delete()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'forbidden'}, status=403)
    except Comment.DoesNotExist:
        return JsonResponse({'status': 'fail'}, status=404)


@csrf_exempt
@login_required
def trip1_add_comment(request):
    """添加评论（trip1页面专用）"""
    if not request.user.is_superuser:
        return JsonResponse({'error': '仅管理员可发表评论'}, status=403)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image')
        video = request.FILES.get('video')
        if image:
            ext = os.path.splitext(image.name)[-1]
            image.name = f"{uuid.uuid4().hex}{ext}"
        if video:
            ext = os.path.splitext(video.name)[-1]
            video.name = f"{uuid.uuid4().hex}{ext}"
        if content or image or video:
            Comment.objects.create(content=content, image=image, video=video, user=request.user, page='trip1')
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'fail', 'message': '只支持POST请求'})


@csrf_exempt
@require_POST
@login_required
def trip1_delete_comment(request, comment_id):
    """删除评论（trip1页面专用）"""
    try:
        comment = Comment.objects.get(id=comment_id)
        if comment.page != 'trip1':
            return JsonResponse({'status': 'forbidden'}, status=403)
        if comment.user == request.user or request.user.is_superuser:
            comment.delete()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'forbidden'}, status=403)
    except Comment.DoesNotExist:
        return JsonResponse({'status': 'fail'}, status=404)


@csrf_exempt
@login_required
def add_comment_generic(request, page_name):
    """通用添加评论视图"""
    # 权限检查
    if not request.user.is_superuser:
        return JsonResponse({
            'status': 'fail',
            'error': '仅管理员可发表评论',
            'message': '您当前没有发表评论的权限，请联系管理员'
        }, status=403)
    
    if request.method != 'POST':
        return JsonResponse({'status': 'fail', 'message': '只支持POST请求'}, status=405)
    
    try:
        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image')
        video = request.FILES.get('video')
        
        # 重命名图片文件
        if image:
            ext = os.path.splitext(image.name)[-1]
            image.name = f"{uuid.uuid4().hex}{ext}"
        
        # 重命名视频文件
        if video:
            ext = os.path.splitext(video.name)[-1]
            video.name = f"{uuid.uuid4().hex}{ext}"
        
        # 创建评论
        if content or image or video:
            Comment.objects.create(
                content=content, 
                image=image, 
                video=video, 
                user=request.user, 
                page=page_name
            )
            return JsonResponse({'status': 'ok', 'message': '评论发表成功'})
        else:
            return JsonResponse({
                'status': 'fail',
                'message': '评论内容、图片或视频至少需要提供一项'
            }, status=400)
            
    except Exception as e:
        return JsonResponse({
            'status': 'fail',
            'error': str(e),
            'message': '评论发表失败，请稍后重试'
        }, status=500)


@csrf_exempt
@require_POST
@login_required
def delete_comment_generic(request, page_name, comment_id):
    """通用删除评论视图"""
    try:
        comment = Comment.objects.get(id=comment_id)
        if comment.page != page_name:
            return JsonResponse({'status': 'forbidden'}, status=403)
        if comment.user == request.user or request.user.is_superuser:
            comment.delete()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'forbidden'}, status=403)
    except Comment.DoesNotExist:
        return JsonResponse({'status': 'fail'}, status=404)

