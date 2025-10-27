from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CustomLoginForm(AuthenticationForm):
    """自定义登录表单，提供中文错误信息"""
    username = forms.CharField(
        label="用户名",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': '请输入用户名'
        }),
        error_messages={
            'required': '请输入用户名',
        }
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': '请输入密码'
        }),
        error_messages={
            'required': '请输入密码',
        }
    )

    error_messages = {
        'invalid_login': '用户名或密码错误，请检查后重试',
        'inactive': '此账号已被停用',
    }

class CustomRegisterForm(UserCreationForm):
    username = forms.CharField(
        label="用户名",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': '请输入用户名'
        }),
        error_messages={
            'required': '请输入用户名',
            'unique': '该用户名已被使用，请选择其他用户名',
        }
    )
    password1 = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': '请输入密码'
        }),
        error_messages={
            'required': '请输入密码',
        }
    )
    password2 = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': '请再次输入密码'
        }),
        error_messages={
            'required': '请再次输入密码',
        }
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('该用户名已被使用，请选择其他用户名')
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1 and len(password1) < 4:
            raise ValidationError('密码长度不能少于4位')
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('两次输入的密码不一致，请重新输入')
        return password2