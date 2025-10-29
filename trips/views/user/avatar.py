"""
用户头像上传视图
"""
import os
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


@csrf_exempt
@login_required
def upload_avatar(request):
    """上传头像"""
    if request.method == 'POST' and request.FILES.get('avatar'):
        avatar_file = request.FILES['avatar']
        
        # 验证文件类型
        if not avatar_file.content_type.startswith('image/'):
            return JsonResponse({'success': False, 'error': '请上传图片文件'})
        
        # 验证文件大小 (5MB)
        if avatar_file.size > 5 * 1024 * 1024:
            return JsonResponse({'success': False, 'error': '图片大小不能超过5MB'})
        
        try:
            # 生成唯一文件名
            ext = os.path.splitext(avatar_file.name)[-1]
            avatar_file.name = f"{uuid.uuid4().hex}{ext}"
            
            # 更新用户头像
            profile = request.user.profile
            
            # 删除旧头像文件（如果存在）
            if profile.avatar:
                try:
                    os.remove(profile.avatar.path)
                except:
                    pass
            
            profile.avatar = avatar_file
            profile.save()
            
            return JsonResponse({
                'success': True, 
                'avatar_url': profile.avatar.url,
                'message': '头像上传成功！'
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'上传失败：{str(e)}'})
    
    return JsonResponse({'success': False, 'error': '请选择要上传的图片'})

