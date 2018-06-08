"""CollabOER URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from . import views

urlpatterns = [
	path('',views.homepage,name="home"),
	path('show/',views.login,name="login"),
	path('show1/',views.logout,name="logout"),
	path('show2/',views.create_community,name="create-community"),
	path('show3/',views.create_sub_community,name="create-sub-community"),
	path('show4/',views.create_collection,name="create-collection"),
	path('show5/',views.insert_item,name="add-items"),
	path('show6/',views.insert_bitstream,name="add-bitstream"),
    path('admin/', admin.site.urls),
]
