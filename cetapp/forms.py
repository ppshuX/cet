from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CustomRegisterForm(UserCreationForm):
    username = forms.CharField(
            label="用户名",
            max_length=150,
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'})
            )
    password1 = forms.CharField(
            label="密码",
            widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'})
            )
    password2 = forms.CharField(
            label="确认密码",
            widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请再次输入密码'})
            )

    def clean_password1(self):
        pwd = self.cleaned_data.get("password1")
        # 自定义宽松规则（如只要 >= 4 位即可）
        if len(pwd) < 4:
            raise ValidationError("密码不能少于4位")
        return pwd

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

