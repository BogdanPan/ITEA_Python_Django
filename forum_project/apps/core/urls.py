from .views import article_view, ArticlesView, MainPageView, ArticleView
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path('', MainPageView.as_view(), name='index'),
    path('articles/<slug:slug>', ArticleView.as_view(), name='articles-article'),
    path('articles/', ArticlesView.as_view(), name='articles'),
]
