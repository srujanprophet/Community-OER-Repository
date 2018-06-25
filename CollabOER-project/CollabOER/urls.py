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
from converter import views as converter_views

urlpatterns = [
	path('',views.homepage,name="home"),
	#path('logindash/',views.logindash,name="logindashboard"),
	#path('CC/',views.ccDashboard,name="ccdashboard"),
	#path('dspace/',views.dspaceDashboard, name="dspacedashboard"),

	#path('getcommunity/',views.get_communities, name="getCommunity"),
	#path('getcommunityarticles/',views.get_community_articles, name="getCommunityArticles"),
	#path('getgroup/',views.get_groups, name="getGroup"),
	#path('getgrouparticles/',views.get_group_articles, name="getGroupArticles"),

	#path('login/',views.login, name="login"),
	#path('logout/',views.logout,name="logout"),

	path('createcommunity/',views.create_community,name="createCommunity"),
	path('createcommunityarticles/',views.create_community_resources,name="createCommunityArticle"),
	path('creategroup/',views.create_groups,name="createGroup"),
	path('creategrouparticles/',views.create_group_resources,name="createGroupArticle"),

	path('render/pdf/',converter_views.Pdf.as_view(), name="convert"),
    path('admin/', admin.site.urls),
]
