import os
import uuid
import json
import urllib3
import requests
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

def main_menu(request):
    return render(request, 'cetapp/index.html')

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
            return redirect('/cetapp/trip1/')  # 注册完跳转到trip1
    else:
        form = CustomRegisterForm()
    return render(request, 'cetapp/register.html', {'form': form})

def get_quote(request):
    try:
        response = requests.get("https://zenquotes.io/api/random", timeout=5)
        data = response.json()[0]  # 它返回的是数组
        return JsonResponse({
            "content": data.get("q", "No content."),
            "author": data.get("a", "Anonymous"),
        })
    except Exception as e:
        return JsonResponse({
            "content": "We travel not to escape life, but for life not to escape us.",
            "author": "Anonymous",
        })

def trip_page(request):
    stats = SiteStat.objects.filter(page='trip').first()
    if not stats:
        stats = SiteStat.objects.create(page='trip')
    stats.views += 1
    stats.save()
    comments = Comment.objects.filter(page='trip').order_by('-timestamp')
    return render(request, 'cetapp/trip.html', {
        'comments': comments,
        'stats': stats,
    })

def trip1(request):
    stats = SiteStat.objects.filter(page='trip1').first()
    if not stats:
        stats = SiteStat.objects.create(page='trip1')
    stats.views += 1
    stats.save()
    comments = Comment.objects.filter(page='trip1').order_by('-timestamp')
    return render(request, 'cetapp/trip1.html', {
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
        page = request.POST.get('page', 'trip')
        if image:
            ext = os.path.splitext(image.name)[-1]
            image.name = f"{uuid.uuid4().hex}{ext}"
        if content or image:
            Comment.objects.create(content=content, image=image, user=request.user, page=page)
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'fail', 'message': '只支持POST请求'})

@csrf_exempt
def like_view(request):
    stats = SiteStat.objects.filter(page='trip').first()
    if not stats:
        stats = SiteStat.objects.create(page='trip')
    stats.likes += 1
    stats.save()
    return JsonResponse({'likes': stats.likes})

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
        if comment.page != 'trip':
            return JsonResponse({'status': 'forbidden'}, status=403)
        if comment.user == request.user or request.user.is_superuser:
            comment.delete()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'forbidden'}, status=403)
    except Comment.DoesNotExist:
        return JsonResponse({'status': 'fail'}, status=404)

def trip_views_likes(request):
    stats = SiteStat.objects.filter(page='trip').first()
    if not stats:
        stats = SiteStat.objects.create(page='trip')
    return JsonResponse({'views': stats.views, 'likes': stats.likes})

@csrf_exempt
def trip1_like_view(request):
    stats = SiteStat.objects.filter(page='trip1').first()
    if not stats:
        stats = SiteStat.objects.create(page='trip1')
    stats.likes += 1
    stats.save()
    return JsonResponse({'likes': stats.likes})

@csrf_exempt
@login_required
def trip1_add_comment(request):
    if not request.user.is_superuser:
        return JsonResponse({'error': '仅管理员可发表评论'}, status=403)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image')
        if image:
            ext = os.path.splitext(image.name)[-1]
            image.name = f"{uuid.uuid4().hex}{ext}"
        if content or image:
            Comment.objects.create(content=content, image=image, user=request.user, page='trip1')
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'fail', 'message': '只支持POST请求'})

@csrf_exempt
@require_POST
@login_required
def trip1_delete_comment(request, comment_id):
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

def trip1_views_likes(request):
    stats = SiteStat.objects.filter(page='trip1').first()
    if not stats:
        stats = SiteStat.objects.create(page='trip1')
    return JsonResponse({'views': stats.views, 'likes': stats.likes})


def trip_page_generic(request, page_name):
    stats = SiteStat.objects.filter(page=page_name).first()
    if not stats:
        stats = SiteStat.objects.create(page=page_name)
    stats.views += 1
    stats.save()
    comments = Comment.objects.filter(page=page_name).order_by('-timestamp')
    return render(request, f'cetapp/{page_name}.html', {
        'comments': comments,
        'stats': stats,
        'page_name': page_name,
    })

@csrf_exempt
def views_likes_generic(request, page_name):
    stats = SiteStat.objects.filter(page=page_name).first()
    if not stats:
        stats = SiteStat.objects.create(page=page_name)
    return JsonResponse({'views': stats.views, 'likes': stats.likes})

@csrf_exempt
@login_required
def add_comment_generic(request, page_name):
    if not request.user.is_superuser:
        return JsonResponse({'error': '仅管理员可发表评论'}, status=403)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image')
        if image:
            ext = os.path.splitext(image.name)[-1]
            image.name = f"{uuid.uuid4().hex}{ext}"
        if content or image:
            Comment.objects.create(content=content, image=image, user=request.user, page=page_name)
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'fail', 'message': '只支持POST请求'})

@csrf_exempt
def like_view_generic(request, page_name):
    stats = SiteStat.objects.filter(page=page_name).first()
    if not stats:
        stats = SiteStat.objects.create(page=page_name)
    stats.likes += 1
    stats.save()
    return JsonResponse({'likes': stats.likes})

@csrf_exempt
@require_POST
@login_required
def delete_comment_generic(request, page_name, comment_id):
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

@csrf_exempt
def checkin_view_generic(request, page_name):
    stats = SiteStat.objects.filter(page=page_name).first()
    if not stats:
        stats = SiteStat.objects.create(page=page_name)
    stats.checked_in = True
    stats.save()
    return JsonResponse({'checked_in': True})

@csrf_exempt
def trip2_like_view(request):
    stats = SiteStat.objects.filter(page='trip2').first()
    if not stats:
        stats = SiteStat.objects.create(page='trip2')
    stats.likes += 1
    stats.save()
    return JsonResponse({'likes': stats.likes})

@csrf_exempt
def trip3_like_view(request):
    stats = SiteStat.objects.filter(page='trip3').first()
    if not stats:
        stats = SiteStat.objects.create(page='trip3')
    stats.likes += 1
    stats.save()
    return JsonResponse({'likes': stats.likes})

def trip2(request):
    return trip_page_generic(request, 'trip2')

def trip4(request):
    return trip_page_generic(request, 'trip4')