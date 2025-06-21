from django.contrib import admin
from .models import Comment, SiteStat

# Register your models here.

admin.site.register(Comment)
admin.site.register(SiteStat)
