"""
基础页面视图（首页、主菜单、CET考试相关页面等）
"""
from django.shortcuts import render


def index(request):
    """网站首页"""
    return render(request, 'index.html')


def main_menu(request):
    """主菜单页面"""
    return render(request, 'cetapp/index.html')


def listening(request):
    """听力页面"""
    return render(request, 'listening.html')


def reading(request):
    """阅读页面"""
    return render(request, 'reading.html')


def writing(request):
    """写作页面"""
    return render(request, 'writing.html')


def translate(request):
    """翻译页面"""
    return render(request, 'translate.html')

