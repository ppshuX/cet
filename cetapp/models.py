from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#评论模型
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 谁发的评论
    content = models.TextField()
    image = models.ImageField(upload_to='comment_images/', blank=True, null=True)  # 新增的图片字段
    timestamp = models.DateTimeField(auto_now_add=True)

#网站统计模型
class SiteStat(models.Model):
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    checked_in = models.BooleanField(default=False)
