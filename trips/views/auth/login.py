"""
用户登录视图
"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from ...forms import CustomLoginForm


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

