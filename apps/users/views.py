from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from apps.users.models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm
from apps.utils.email_utils import send_register_email


class CustomBackend(ModelBackend):
    """
    自定义用户登录的方式
    可以用户名和邮箱登录
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username = username)|Q(email=username))
            if user.check_password(password):
               return user
        except Exception as e:
            return None


class ActiveView(View):
    """
    处理激活的View
    """
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        return render(request, 'login.html')

class LoginView(View):
    """
    处理登录的View
    /login/
    """
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html', {})
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或者密码错误'})
        else:
            return render(request, 'login.html', {'login_form':login_form})


class RegisterView(View):
    """
    处理注册的View
    """
    def get(self,request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form':register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get('email', '')
            password = request.POST.get('password', '')

            # 判断是否邮箱已经注册
            if UserProfile.objects.filter(email=username):
                return render(request, 'register.html', {'register_form': register_form, 'msg':'邮箱已经注册'})

            user_profile = UserProfile()
            user_profile.username = username
            user_profile.email = username
            user_profile.is_active = False
            user_profile.password = make_password(password)
            user_profile.save()
            send_register_email(user_profile.email, 'register')
            return render(request, 'login.html', {})
        else:
            return render(request, 'register.html', {'register_form':register_form})

class ForgetPwdView(View):
    """
    处理忘记密码的View
    """
    def get(self, request):
        forgetPwdForm = ForgetPwdForm()
        # return render(request, 'index.html')
        return render(request, 'forgetpwd.html', {'forgetPwd_form':forgetPwdForm})

    def post(self, request):
        forgetPwdForm = ForgetPwdForm(request.POST)
        if forgetPwdForm.is_valid():
            email = request.POST.get("email", "")
            user = UserProfile.objects.filter(email=email)

            # 用户存在且已经激活的话可以修改密码
            if user:
                user = UserProfile.objects.get(email=email)
                if user.is_active:
                    send_register_email(email, 'forget')
                    return render(request, 'sendsuccess.html')
                else:
                    return render(request, 'forgetpwd.html', {'forgetPwd_form': forgetPwdForm, 'msg': '用户未激活'})
            else:
                return render(request, 'forgetpwd.html', {'forgetPwd_form': forgetPwdForm, 'msg':'用户不存在'})
        else:
            return render(request, 'forgetpwd.html', {'forgetPwd_form': forgetPwdForm})


class ResetView(View):
    """
    处理重置密码的View，带有active_code参数
    """
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'resetpwd.html', {'email':email})
        return render(request, 'login.html')


class ModifyPwdView(View):
    """
    处理修改密码的View
    """
    def post(self, request):
        modifyPwdForm = ModifyPwdForm(request.POST)
        if modifyPwdForm.is_valid():
            password1 = request.POST.get("password1", "")
            password2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if password1 != password2:
                return render(request, 'resetpwd.html', {'email':email, 'modifyPwdForm':modifyPwdForm, 'msg':'密码前后不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(password1)
            user.save()
            return render(request, 'login.html', {'msg':'密码重置成功，请登录'})
        else:
            email = request.POST.get("email", "")
            return render(request, 'resetpwd.html', {'email':email, 'modifyPwdForm':modifyPwdForm})