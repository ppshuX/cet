"""
用户中心相关视图
"""
import os
import uuid
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User


@login_required
def user_center(request):
    """用户个人中心"""
    if request.method == 'POST':
        # 处理个人信息更新
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        
        # 验证用户名唯一性
        if username != request.user.username:
            if User.objects.filter(username=username).exists():
                messages.error(request, '用户名已存在，请选择其他用户名')
                return redirect('user_center')
        
        # 更新用户信息
        request.user.username = username
        request.user.email = email
        request.user.save()
        
        messages.success(request, '个人信息更新成功！')
        return redirect('user_center')
    
    # 简单的上下文数据
    context = {}
    
    return render(request, 'cetapp/user_center.html', context)


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

