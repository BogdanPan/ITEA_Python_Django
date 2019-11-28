from django.contrib import admin
from .models import Article, Comment
from django.utils.html import format_html


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'show_text', 'show_img')
	list_display_links = ('id', 'title', 'show_text', 'show_img')
	readonly_fields = ('slug', 'created', 'updated',)

	@staticmethod
	def show_text(obj):
		if len(obj.text) <= 100:
			return obj.text
		else:
			return f"{obj.text[:100]}..."

	@staticmethod
	def show_img(obj):
		if obj.image:
			return format_html(f'<img src={obj.image.url} width="60" height="60">')
		else:
			return format_html(f'')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('id', 'article', 'user', 'show_text')
	list_display_links = ('id', 'article', 'user', 'show_text')
	readonly_fields = ('created', 'updated',)

	@staticmethod
	def show_text(obj):
		if len(obj.text) <= 100:
			return obj.text
		else:
			return f"{obj.text[:100]}..."
