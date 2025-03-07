"""techk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path
from rest_framework import routers

from apps.base.views import BookView, CategoryView
from apps.scraper.views import ScraperView

router = routers.DefaultRouter()
router.register(r'book', BookView, 'book')
router.register(r'category', CategoryView, 'category')

urlpatterns = [
    path('scraper/', ScraperView.as_view(), name='scraper'),
]

urlpatterns += router.urls
