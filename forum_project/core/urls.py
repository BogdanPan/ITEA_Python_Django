from django.urls import path
from .views import index, article, articles
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index),
    path('articles/<str:article_name>', article),
    path('articles/', articles)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
