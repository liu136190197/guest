"""guest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url, include

from sign import views, views_if_security
from sign import views_if
from sign import views_if_sec

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),#添加 index/路径配置
    path('accounts/login/', views.index),#添加 accounts/login/路径配置,登录失败时返回登陆页
    path('login_action/', views.login_action),#添加 login_action/路径配置
    path('logout/', views.logout),#添加 logout/路径配置
    path('event_manage/', views.event_manage),#添加 event_manage/路径配置
    path('search_name_event/', views.search_name_event),  #添加搜索功能
    path('guest_manage/', views.guest_manage),  # 添加 guest_manage/路径配置
    path('search_name_guest/', views.search_name_guest),  #添加搜索功能
    re_path(r'sign_index/(?P<event_id>[0-9]+)/$', views.sign_index),  #添加签到功能
    re_path(r'sign_index_action/(?P<event_id>[0-9]+)/$', views.sign_index_action),  #添加签到动作

    path(r'api/', include(('sign.urls','sign'), namespace="sign")),#web接口基本路径

]
