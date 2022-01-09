"""FoodDistribution URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from FoodDistribution import settings
from apps.order_manage.views import OrderViewSet
from apps.user_manage.views import UserViewSet

if settings.DEBUG:
    router_v1 = DefaultRouter()
else:
    router_v1 = SimpleRouter()

router_v1.register(r'user', UserViewSet, basename='user')
router_v1.register(r'order', OrderViewSet, basename='order')


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/v1/', include(router_v1.urls)),
]
