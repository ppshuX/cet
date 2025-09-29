from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Comment, SiteStat, UserProfile, CommentLike

# Register your models here.

# 内联显示UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = '用户配置'
    fields = ('avatar',)

# 自定义User管理界面
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')

# 重新注册User模型
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# 单独注册UserProfile（可选）
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar')
    search_fields = ('user__username', 'user__email')

admin.site.register(Comment)
admin.site.register(SiteStat)
admin.site.register(CommentLike)
