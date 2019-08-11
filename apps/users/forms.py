from django import forms
from django.forms import Form
from captcha.fields import CaptchaField


class LoginForm(Form):
    """
    登录验证表单
    """
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=8)


class RegisterForm(Form):
    """
    注册表单
    """
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=8)
    captcha = CaptchaField(error_messages={"invalid":"验证码错误"})
    #captcha = CaptchaField()

class ForgetPwdForm(Form):
    """
    忘记密码表单
    """
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid":"验证码错误"})

class ModifyPwdForm(Form):
    """
    修改密码表单
    """
    email = forms.EmailField(required=True)
    password1 = forms.CharField(required=True, min_length=8)
    password2 = forms.CharField(required=True, min_length=8)