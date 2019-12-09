from django.urls import path
from rest_framework import routers
from .views import ArticleAPIView

urlpatterns = [
    path('article/', ArticleAPIView.as_view(), name='article'),
]
