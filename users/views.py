from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import render,redirect
from django.contrib.auth import  login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.models import User
import random
@login_required(login_url='/users/login1.html')
def logout_view(request):
    """注销用户"""
    logout(request)
    return HttpResponseRedirect(reverse('index:index'))

def register(request):
    '''注册新用户'''
    if request.method!='POST':
        form=UserCreationForm()

    else:
        #处理填写好的表单
        form=UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user=form.save()
            #让用户自动登陆，在重定向到主页
            authenticate_user=authenticate(username=new_user.username,password=request.POST['password1'])
            login(request,authenticate_user)
            return HttpResponseRedirect(reverse('index:index'))
    context={'form':form}
    tips='注册成功，请登录'
    return render(request,'users/register.html',context,locals())

@login_required()
def setpasswordView(request):
    title='修改密码'
    unit_2='/users/login1.html'
    unit_2_name='立即登录'
    unit_1='/users/findpassword.html'
    unit_1_name='忘记密码'

    new_password = True
    if request.method == 'POST':
        username = request.POST.get('username', '')
        old_password = request.POST.get('password', '')
        new_password = request.POST.get('new_password', '')
        # 判断用户是否存在
        user = User.objects.filter(username=username)
        if User.objects.filter(username=username):
            user = authenticate(username=username, password=old_password)
            # 判断用户的账号密码是否正确
            if user:
                # 密码加密处理并保存到数据库
                dj_ps = make_password(new_password, None, 'pbkdf2_sha256')
                user.password = dj_ps
                user.save()
                tips='密码修改成功'
            else:
                tips='原始密码不正确'
        else:
            tips='用户不存在'
    return render(request, 'users/user.html', locals())

# 找回密码
def findpassword(request):
    button = '获取验证码'
    new_password = False
    if request.method == 'POST':
        username = request.POST.get('username', 'root')
        VerificationCode = request.POST.get('VerificationCode', '')
        password = request.POST.get('password', '')
        user = User.objects.filter(username=username)
        # 用户不存在
        if not user:
            tips = '用户' + username + '不存在'
        else:
            # 判断验证码是否已发送
            if not request.session.get('VerificationCode', ''):
                # 发送验证码并将验证码写入session
                button = '重置密码'
                tips = '验证码已发送'
                new_password = True
                VerificationCode = str(random.randint(100000, 999999))
                request.session['VerificationCode'] = VerificationCode
                user[0].email_user('找回密码', VerificationCode)
            # 匹配输入的验证码是否正确
            elif VerificationCode == request.session.get('VerificationCode'):
                # 密码加密处理并保存到数据库
                dj_ps = make_password(password, None, 'pbkdf2_sha256')
                user[0].password = dj_ps
                user[0].save()
                del request.session['VerificationCode']
                tips = '密码已重置'
            # 输入验证码错误
            else:
                tips = '验证码错误，请重新获取'
                new_password = False
                del request.session['VerificationCode']
    return render(request, 'users/findpassword.html', locals())

# 用户登录
def loginView(request):
    # 设置标题和另外两个URL链接
    title = '登录'
    unit_2 = '/users/register.html'
    unit_2_name = '立即注册'
    unit_1 = '/users/findpassword.html'
    unit_1_name = '忘记密码？'
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if User.objects.filter(username=username):
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                return redirect('/')
            else:
                tips = '账号密码错误，请重新输入'
        else:
            tips = '用户不存在，请注册'
    return render(request, 'users/login1.html', locals())

def homeView(request):


    return render(request, 'users/home.html', locals())


