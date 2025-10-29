"""
用户注册视图
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login
from ...forms import CustomRegisterForm


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

