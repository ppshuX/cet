"""
头像下载工具
用于从QQ等第三方平台下载头像并设置为用户头像
"""
import os
import requests
import uuid
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
import sys


def download_avatar_from_url(avatar_url):
    """
    从URL下载头像图片
    
    Args:
        avatar_url: 头像URL
        
    Returns:
        tuple: (成功标志, 图片文件对象或错误信息)
    """
    if not avatar_url:
        return False, "头像URL为空"
    
    try:
        # 下载图片
        response = requests.get(avatar_url, timeout=10, stream=True)
        response.raise_for_status()
        
        # 检查Content-Type
        content_type = response.headers.get('Content-Type', '')
        if not content_type.startswith('image/'):
            return False, "URL返回的不是图片"
        
        # 读取图片数据
        image_data = BytesIO(response.content)
        
        # 验证是否为有效图片
        try:
            img = Image.open(image_data)
            img.verify()  # 验证图片完整性
        except Exception:
            return False, "无效的图片格式"
        
        # 重新打开图片（verify会关闭文件）
        image_data.seek(0)
        img = Image.open(image_data)
        
        # 转换为RGB（处理PNG等格式）
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # 裁剪为正方形
        min_side = min(img.width, img.height)
        left = (img.width - min_side) // 2
        top = (img.height - min_side) // 2
        right = left + min_side
        bottom = top + min_side
        img = img.crop((left, top, right, bottom))
        
        # 调整为300x300像素（与UserProfile的save方法一致）
        img = img.resize((300, 300), Image.Resampling.LANCZOS)
        
        # 保存到内存
        output = BytesIO()
        img.save(output, format='JPEG', quality=90)
        output.seek(0)
        
        # 创建文件名
        filename = f"{uuid.uuid4().hex}.jpg"
        
        # 创建Django File对象
        django_file = InMemoryUploadedFile(
            output,
            None,
            filename,
            'image/jpeg',
            sys.getsizeof(output),
            None
        )
        
        return True, django_file
        
    except requests.exceptions.RequestException as e:
        return False, f"下载失败: {str(e)}"
    except Exception as e:
        return False, f"处理失败: {str(e)}"


def set_user_avatar_from_url(user, avatar_url):
    """
    从URL下载头像并设置为用户头像
    
    Args:
        user: User对象
        avatar_url: 头像URL
        
    Returns:
        tuple: (成功标志, 消息)
    """
    if not hasattr(user, 'profile'):
        return False, "用户没有profile"
    
    success, result = download_avatar_from_url(avatar_url)
    
    if not success:
        return False, result
    
    try:
        # 删除旧头像（如果存在）
        if user.profile.avatar:
            try:
                if os.path.isfile(user.profile.avatar.path):
                    os.remove(user.profile.avatar.path)
            except:
                pass  # 忽略删除失败
        
        # 设置新头像
        user.profile.avatar = result  # result是Django File对象
        user.profile.save()  # save会自动处理图片压缩
        
        return True, "头像设置成功"
        
    except Exception as e:
        return False, f"保存头像失败: {str(e)}"

