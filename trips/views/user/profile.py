"""
用户个人中心视图
"""
from django.shortcuts import render, redirect
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
    
    return render(request, 'trips/user_center.html', context)

