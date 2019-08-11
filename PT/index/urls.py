"""PT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from index import views

urlpatterns = [
    path('home/', views.home, name='home'),
    # path('base/', views.base),
    path('success/', views.success),
    path('apitest/', views.apitest),
    path('login/', views.index_login),
    path('register/', views.index_register),
    path('task/', views.index_task),
    path('cases/', views.index_cases),
    path('apk/', views.index_apk),
    path('task/new/', views.index_newtask),
    path('task/update/', views.index_updatetask),
    path('upload_cases/', views.api_uploadcases),
    path('upload_apk/', views.api_upload_apk),
    path('api/user_exist/', views.user_exist),
    path('api/task_exist/', views.task_exist),
    path('api/register/', views.api_register),
    path('api/login/', views.api_login),
    path('api/task_new/', views.api_newtask),
    path('api/get_task/', views.api_gettask),
    path('api/delete_task', views.api_deletetask),
    path('api/guidang_task', views.api_guidangtask),
    path('api/run_cases/', views.api_run_cases),
    path('api/run_apk/', views.api_run_apk),
]
