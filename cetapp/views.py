import os
import uuid
import json
import urllib3
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
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


def custom_login(request):
    """自定义登录视图，提供更好的错误处理"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
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
            # 添加自定义错误信息
            if not form.cleaned_data.get('username'):
                form.add_error('username', '请输入用户名')
            if not form.cleaned_data.get('password'):
                form.add_error('password', '请输入密码')
            if form.cleaned_data.get('username') and form.cleaned_data.get('password'):
                form.add_error(None, '用户名或密码错误，请检查后重试')
    else:
        form = AuthenticationForm()
    
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
    
    # 获取当前用户已点赞的评论ID列表
    user_liked_comments = []
    if request.user.is_authenticated:
        from .models import CommentLike
        user_liked_comments = CommentLike.objects.filter(
            user=request.user,
            comment__in=comments
        ).values_list('comment_id', flat=True)
    
    return render(request, f'cetapp/{page_name}.html', {
        'comments': comments,
        'stats': stats,
        'page_name': page_name,
        'user_liked_comments': list(user_liked_comments),
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
        video = request.FILES.get('video')
        if image:
            ext = os.path.splitext(image.name)[-1]
            image.name = f"{uuid.uuid4().hex}{ext}"
        if video:
            ext = os.path.splitext(video.name)[-1]
            video.name = f"{uuid.uuid4().hex}{ext}"
        if content or image or video:
            Comment.objects.create(content=content, image=image, video=video, user=request.user, page=page_name)
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

# 评论点赞功能
@csrf_exempt
def toggle_comment_like(request, comment_id):
    """切换评论点赞状态"""
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': '请先登录'})
    
    try:
        comment = Comment.objects.get(id=comment_id)
        from .models import CommentLike
        
        # 检查是否已经点赞
        like, created = CommentLike.objects.get_or_create(
            user=request.user,
            comment=comment
        )
        
        if created:
            # 新增点赞
            liked = True
        else:
            # 取消点赞
            like.delete()
            liked = False
        
        # 获取当前点赞总数
        like_count = comment.likes.count()
        
        return JsonResponse({
            'status': 'ok',
            'liked': liked,
            'like_count': like_count
        })
        
    except Comment.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': '评论不存在'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})