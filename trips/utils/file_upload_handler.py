"""
统一文件上传处理器
处理所有媒体文件的上传逻辑：临时保存、上传到COS、删除临时文件
"""
import os
import uuid
import tempfile
from django.utils import timezone
from .tencent_cos import upload_to_cos, delete_from_cos


class FileUploadHandler:
    """文件上传处理器"""
    
    @staticmethod
    def generate_unique_filename(original_filename, prefix=''):
        """
        生成唯一的文件名
        
        Args:
            original_filename (str): 原始文件名
            prefix (str): 文件名前缀（如用户ID）
            
        Returns:
            str: 唯一的文件名
        """
        ext = os.path.splitext(original_filename)[-1].lower()
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        unique_id = uuid.uuid4().hex[:8]
        
        if prefix:
            return f"{prefix}_{timestamp}_{unique_id}{ext}"
        return f"{timestamp}_{unique_id}{ext}"
    
    @staticmethod
    def upload_file(uploaded_file, save_dir='media', filename_prefix=''):
        """
        处理文件上传到 COS
        
        Args:
            uploaded_file: Django UploadedFile 对象
            save_dir (str): COS 中的保存目录（如 'media/avatars'）
            filename_prefix (str): 文件名前缀（如用户ID）
            
        Returns:
            str: 文件的 COS 公网访问 URL
            
        Raises:
            Exception: 上传失败时抛出异常
        """
        temp_file_path = None
        
        try:
            # 生成唯一文件名
            unique_filename = FileUploadHandler.generate_unique_filename(
                uploaded_file.name, 
                prefix=filename_prefix
            )
            
            # 创建临时文件
            temp_dir = tempfile.gettempdir()
            temp_file_path = os.path.join(temp_dir, unique_filename)
            
            # 保存上传的文件到临时目录
            with open(temp_file_path, 'wb+') as temp_file:
                for chunk in uploaded_file.chunks():
                    temp_file.write(chunk)
            
            print(f"临时文件已保存: {temp_file_path}")
            
            # 构建 COS 保存路径
            cos_save_path = f"{save_dir}/{unique_filename}"
            
            # 上传到 COS
            cos_url = upload_to_cos(temp_file_path, cos_save_path)
            
            return cos_url
            
        except Exception as e:
            print(f"文件上传失败: {e}")
            raise
            
        finally:
            # 删除临时文件
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path)
                    print(f"临时文件已删除: {temp_file_path}")
                except Exception as e:
                    print(f"删除临时文件失败: {e}")
    
    @staticmethod
    def delete_file(cos_url):
        """
        从 COS 删除文件
        
        Args:
            cos_url (str): COS 文件的完整 URL
            
        Returns:
            bool: 删除成功返回 True，失败返回 False
        """
        if not cos_url:
            return False
        
        return delete_from_cos(cos_url)
    
    @staticmethod
    def upload_avatar(uploaded_file, user_id):
        """
        上传用户头像
        
        Args:
            uploaded_file: Django UploadedFile 对象
            user_id (int): 用户ID
            
        Returns:
            str: 头像的 COS 公网访问 URL
        """
        return FileUploadHandler.upload_file(
            uploaded_file,
            save_dir='media/avatars',
            filename_prefix=f'user{user_id}'
        )
    
    @staticmethod
    def upload_comment_image(uploaded_file, user_id):
        """
        上传评论图片
        
        Args:
            uploaded_file: Django UploadedFile 对象
            user_id (int): 用户ID
            
        Returns:
            str: 图片的 COS 公网访问 URL
        """
        return FileUploadHandler.upload_file(
            uploaded_file,
            save_dir='media/comments/images',
            filename_prefix=f'user{user_id}'
        )
    
    @staticmethod
    def upload_comment_video(uploaded_file, user_id):
        """
        上传评论视频
        
        Args:
            uploaded_file: Django UploadedFile 对象
            user_id (int): 用户ID
            
        Returns:
            str: 视频的 COS 公网访问 URL
        """
        return FileUploadHandler.upload_file(
            uploaded_file,
            save_dir='media/comments/videos',
            filename_prefix=f'user{user_id}'
        )

