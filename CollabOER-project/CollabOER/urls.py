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
	path('get1/',views.test_get_communities,name="test_get_communities"),
	path('get2/',views.get_community_resources,name="get_community_resources"),
	path('get3/',views.get_groups, name="get_groups"),
	path('get4/',views.get_group_resources, name="get_group_resources"),


	
	path('show/',views.test_login,name="login"),
	path('show1/',views.test_logout,name="logout"),
	path('show2/',views.create_community,name="create-community"),
	path('show3/',views.create_sub_community,name="create-sub-community"),
	path('show4/',views.test_create_collection,name="test_create_collection"),
	path('show5/',views.insert_item,name="add-items"),
	path('show6/',views.insert_bitstream,name="add-bitstream"),
    path('admin/', admin.site.urls),
]
