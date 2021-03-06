"""django_tools URL Configuration

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
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('downloadExcel/<str:filename>/', views.download_excel, name='downloadExcel'),
    path('uploadExcel/', views.upload_excel, name='uploadExcel'),
    path('uploadExcelView/', views.upload_excel_view, name='uploadExcelView'),
    path('head/', views.head, name='head'),
    path('redis/', views.query_key, name='redis'),
    path('cleanUserCache/', views.clean_user_info, name='cleanUserCache'),
    path('serverinfo/', views.server_info, name='serverinfo'),
    path('server_jc/', views.server_jc, name='server_jc'),
    path('upload/', views.upload_file, name='upload'),
    path('uploadview/', views.upload_view, name='uploadview'),
    path('admin/', admin.site.urls),
    url(r'^login/$', views.login),
]

handler404 = views.handle_404

handler500 = views.handle_500

