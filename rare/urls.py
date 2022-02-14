"""rare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls import include
from rest_framework import routers
from rareapi.views import register_user, login_user
from rareapi.views.post import PostView
from rareapi.views.rare_user import RareUserView
from rareapi.views.reaction import ReactionView
from rareapi.views.tag import TagView
from rest_framework import routers
from django.conf.urls import include
from levelupapi.views import register_user, login_user

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'rareusers', RareUserView, 'rareuser')
router.register(r'tags', TagView, 'tag')
router.register(r'posts', PostView, 'post')
router.register(r'reactions', ReactionView, 'reaction')

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]


