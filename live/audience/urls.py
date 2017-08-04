# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views



urlpatterns = [
    url(r'^login/$', views.UserInfoLogin.as_view(), name='login'),
    url(r'^register/$', views.Registration.as_view(), name='register'),  # 注册
    url(r'^get_verification_code/$', views.VerificationCodeView.as_view()),  # 获取验证码
    url(r'^reset_password/$', views.ResetPasswordView.as_view(), name='reset_password'),  # 修改密码




]
