from django.shortcuts import render
from .models import Article
# Create your views here.


def article(request, article_name):
	art = Article.find_by_slug(article_name)
	ctx = {'name': art.a_title, 'text': art.a_text}
	return render(request, 'article.html', ctx)


def index(request):
	ctx = {'articles': Article.objects.all()}
	return render(request, 'main_page.html', ctx)


def articles(request):
	ctx = {'articles': Article.objects.all()}
	return render(request, 'articles.html', ctx)
