from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from apps.core.models import Article

from .serializers import ArticleSerializer


class ArticleAPIView(ListAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ('title',)
    search_fields = ('title',)
    ordering_fields = ('id', 'title')

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)
