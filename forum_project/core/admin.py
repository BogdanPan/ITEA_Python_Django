from django.contrib import admin
from .models import Article
from django.utils.html import format_html


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'show_text', 'show_img')
	list_display_links = ('id', 'title', 'show_text', 'show_img')
	readonly_fields = ('slug', 'created', 'updated',)

	@staticmethod
	def show_text(obj):
		return f"{obj.text[:100]}..."

	@staticmethod
	def show_img(obj):
		return format_html(f'"<img src={obj.image.url} width="60" height="60">"')