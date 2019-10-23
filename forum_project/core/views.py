from django.shortcuts import render
from .models import Article
# Create your views here.


def article(request, article_name):
	art = Article.find_by_name(article_name)
	ctx = {'name': art.article_name, 'text': art.article_text}
	return render(request, 'article.html', ctx)


def index(request):
	ctx = {'articles': Article.objects.all()}
	return render(request, 'main_page.html', ctx)


def articles(request):
	ctx = {'articles': Article.objects.all()}
	return render(request, 'articles.html', ctx)
