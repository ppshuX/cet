import os
import uuid
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import CustomRegisterForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Comment, SiteStat
from django.utils import timezone

# Create your views here.
def index(request):
    return render(request, 'index.html')

def listening(request):
    return render(request, 'listening.html')

def reading(request):
    return render(request, 'reading.html')

def writing(request):
    return render(request, 'writing.html')

def translate(request):
    return render(request, 'translate.html')


def register(request):
    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # 创建用户
            login(request, user)
            return redirect('/cetapp/trip')  # 注册完跳转到登录页
    else:
        form = CustomRegisterForm()
    return render(request, 'cetapp/register.html', {'form': form})


def trip_page(request):
    stats, _ = SiteStat.objects.get_or_create(id=1)
    stats.views += 1
    stats.save()
    comments = Comment.objects.order_by('-timestamp')
    return render(request, 'cetapp/trip.html', {
        'comments': comments,
        'stats': stats,
    })

@csrf_exempt
@login_required
def add_comment(request):
    if not request.user.is_superuser:
        return JsonResponse({'error': '仅管理员可发表评论'}, status=403)

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image')

       # 处理图片中文名的问题
        if image:
            ext = os.path.splitext(image.name)[-1]  # 获取扩展名
            image.name = f"{uuid.uuid4().hex}{ext}"  # 使用随机名避免中文 

        if content or image:
            Comment.objects.create(content=content,image=image, user=request.user)
            return JsonResponse({'status':'ok'})

    return JsonResponse({'status': 'fail', 'message': '只支持POST请求'})

@csrf_exempt
def like_view(request):
    stats = SiteStat.objects.get(id=1)
    stats.likes += 1
    stats.save()
    return JsonResponse({'likes':stats.likes})

@csrf_exempt
def checkin_view(request):
    stats = SiteStat.objects.get(id=1)
    stats.checked_in = True
    stats.save()
    return JsonResponse({'checked_in':True})


@csrf_exempt
@require_POST
@login_required
def delete_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)

        # 权限判断：本人 或 超级用户 才能删除
        if comment.user == request.user or request.user.is_superuser:
            comment.delete()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'forbidden'}, status=403)
    except Comment.DoesNotExist:
        return JsonResponse({'status': 'fail'}, status=404)
