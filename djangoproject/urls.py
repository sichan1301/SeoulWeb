"""djangoproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
import myapp.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',myapp.views.index,name="index"),
    path('login/',myapp.views.login,name="login"),
    path('signup/',myapp.views.signup,name="signup"),
    path('logout/',myapp.views.logout,name="logout"),
    path('loginsuccess/',myapp.views.loginsuccess,name="loginsuccess"),
    path('signupsuccess/',myapp.views.signupsuccess,name="signupsuccess"),
    path('fail/',myapp.views.fail,name="fail"),
    path('change/',myapp.views.change,name="change"),
    path('corona/',myapp.views.corona,name="corona"),
    path('news/',myapp.views.news,name="news"),
    path('read/',myapp.views.read,name="read"),
    path('create/',myapp.views.create,name="create"),
    path('weather/',myapp.views.weather,name="weather"),
    path('subway/',myapp.views.subway,name="subway"),
    path('change_suc/',myapp.views.change_suc,name="change_suc"),
    path('detail/<int:detail_id>',myapp.views.detail,name="detail"),
    path('delete/<int:pk>',myapp.views.delete,name="delete"),
    path('update/<int:pk>',myapp.views.update,name="update"),
    ]
