"""
腾讯云 COS 对象存储上传工具
"""
import os
from qcloud_cos import CosConfig, CosS3Client
from django.conf import settings


def get_cos_client():
    """
    获取腾讯云 COS 客户端实例
    
    需要在 settings.py 中配置以下变量：
    - TENCENT_COS_SECRET_ID: 腾讯云密钥 SecretId
    - TENCENT_COS_SECRET_KEY: 腾讯云密钥 SecretKey
    - TENCENT_COS_REGION: COS 区域，如 'ap-guangzhou'
    - TENCENT_COS_BUCKET: 存储桶名称
    """
    config = CosConfig(
        Region=settings.TENCENT_COS_REGION,
        SecretId=settings.TENCENT_COS_SECRET_ID,
        SecretKey=settings.TENCENT_COS_SECRET_KEY,
        Token=None,
        Scheme='https'
    )
    client = CosS3Client(config)
    return client


def upload_to_cos(file_path, save_path):
    """
    上传文件到腾讯云 COS
    
    Args:
        file_path (str): 本地文件路径（如 /tmp/xxx.jpg）
        save_path (str): COS 中的保存路径（如 media/avatars/xxx.jpg）
    
    Returns:
        str: 文件的公网访问 URL（如 https://xxxx.cos.ap-guangzhou.myqcloud.com/media/avatars/xxx.jpg）
        
    Raises:
        Exception: 上传失败时抛出异常
    """
    try:
        client = get_cos_client()
        bucket = settings.TENCENT_COS_BUCKET
        
        # 确保 save_path 不以 / 开头（COS 要求）
        if save_path.startswith('/'):
            save_path = save_path[1:]
        
        # 上传文件
        with open(file_path, 'rb') as fp:
            response = client.put_object(
                Bucket=bucket,
                Body=fp,
                Key=save_path,
                EnableMD5=False
            )
        
        # 构建公网访问 URL
        url = f"https://{bucket}.cos.{settings.TENCENT_COS_REGION}.myqcloud.com/{save_path}"
        
        print(f"文件上传成功: {file_path} -> {url}")
        return url
        
    except Exception as e:
        print(f"COS 上传失败: {e}")
        raise Exception(f"文件上传到 COS 失败: {str(e)}")


def delete_from_cos(cos_url):
    """
    从腾讯云 COS 删除文件
    
    Args:
        cos_url (str): COS 文件的完整 URL
        
    Returns:
        bool: 删除成功返回 True，失败返回 False
    """
    try:
        client = get_cos_client()
        bucket = settings.TENCENT_COS_BUCKET
        
        # 从 URL 中提取文件路径（Key）
        # URL 格式: https://bucket.cos.region.myqcloud.com/path/to/file.jpg
        # 需要提取 path/to/file.jpg 部分
        parts = cos_url.split(f"{bucket}.cos.{settings.TENCENT_COS_REGION}.myqcloud.com/")
        if len(parts) < 2:
            print(f"无效的 COS URL: {cos_url}")
            return False
        
        file_key = parts[1]
        
        # 删除文件
        response = client.delete_object(
            Bucket=bucket,
            Key=file_key
        )
        
        print(f"文件删除成功: {cos_url}")
        return True
        
    except Exception as e:
        print(f"COS 删除失败: {e}")
        return False

