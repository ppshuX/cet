import os
import uuid
import json
import urllib3
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomRegisterForm, CustomLoginForm
from django.shortcuts import render, redirect
from .models import Comment, SiteStat
from django.utils import timezone
from django.contrib.auth.models import User

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
                next_url = request.GET.get('next', 'cetapp_main_menu')
                return redirect(next_url)
    else:
        form = CustomLoginForm()
    
    return render(request, 'registration/login.html', {'form': form})

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

def custom_logout(request):
    """自定义登出视图，支持next参数跳转"""
    logout(request)
    # 获取next参数，如果没有就跳转到首页
    next_url = request.GET.get('next') or request.POST.get('next') or '/'
    return redirect(next_url)

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

@csrf_exempt
def trip4_like_view(request):
    stats = SiteStat.objects.filter(page='trip4').first()
    if not stats:
        stats = SiteStat.objects.create(page='trip4')
    stats.likes += 1
    stats.save()
    return JsonResponse({'likes': stats.likes})

# 个人中心相关视图
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
            import uuid
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
