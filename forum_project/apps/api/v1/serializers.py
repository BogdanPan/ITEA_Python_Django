from rest_framework import serializers
from apps.core.models import Article


# class CategorySerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(max_length=255)
#     slug = serializers.SlugField(read_only=True)

#     def create(self, validated_data):
#         return Category.objects.create(**validated_data)


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('created', 'updated',)
