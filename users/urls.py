from django.contrib.auth.views import LoginView
from django.conf.urls import url

from . import views

app_name = 'users'
 
urlpatterns = [
    #登录页面
	#url(r'^login/$', login, {'template_name': 'users/login.html'}, name = 'login'),
	#url(r'^login/$', LoginView.as_view(template_name='users/login.html'), name="login"),
    url('login1.html',views.loginView,name='login1'),
    # 注销
    url(r'^logout/$', views.logout_view, name='logout'),
    # 注册页面
    url(r'register.html', views.register, name='register'),

    url('setpassword.html',views.setpasswordView,name='setpassword'),
    url('findpassword.html',views.findpassword,name='findpassword'),
    url('home.html',views.homeView,name='home'),

]
