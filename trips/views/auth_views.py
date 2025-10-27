"""
用户认证相关视图
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from ..forms import CustomRegisterForm, CustomLoginForm


def custom_login(request):
    """自定义登录视图，提供中文错误信息"""
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # 重定向到用户想要访问的页面，或默认页面
                next_url = request.GET.get('next', 'trips_main_menu')
                return redirect(next_url)
    else:
        form = CustomLoginForm()
    
    return render(request, 'registration/login.html', {'form': form})


def register(request):
    """用户注册视图"""
    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # 创建用户
            login(request, user)
            return redirect('/trips/trip1/')  # 注册完跳转到trip1
    else:
        form = CustomRegisterForm()
    return render(request, 'trips/register.html', {'form': form})


def custom_logout(request):
    """自定义登出视图，支持next参数跳转"""
    logout(request)
    # 获取next参数，如果没有就跳转到首页
    next_url = request.GET.get('next') or request.POST.get('next') or '/'
    return redirect(next_url)

