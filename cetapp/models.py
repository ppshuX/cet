from django.db import models

# Create your models here.
#评论模型
class Comment(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_owner = models.BooleanField(default=True)

#网站统计模型
class SiteStat(models.Model):
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    checked_in = models.BooleanField(default=False)
