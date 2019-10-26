from django.shortcuts import render
from .models import Article
# Create your views here.


def article(request, article_name):
	art = Article.find_by_slug(article_name)
	if art:
		ctx = {'name': art.title, 'text': art.text}
		return render(request, 'article.html', ctx)
	else:
		return render(request, 'error404.html')


def index(request):
	query = Article.objects.all().order_by('-created')
	if len(query) <= 5:
		ctx = {'articles': query}
	else:
		ctx = {'articles': query[:5]}

	return render(request, 'main_page.html', ctx)


def articles(request):
	ctx = {'articles': Article.objects.all()}
	return render(request, 'articles.html', ctx)
