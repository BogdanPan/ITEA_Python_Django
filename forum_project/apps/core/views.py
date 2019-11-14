from django.shortcuts import render
from .models import Article, Comment
from ..core.forms import CommentForm
from django.views.generic import View, TemplateView, ListView, DetailView, RedirectView, CreateView
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse


class MainPageView(TemplateView):
	template_name = 'core/main_page.html'

	def get_context_data(self, **kwargs):
		query = Article.objects.all().order_by('-created')
		context = ({'articles': query, 'number_of_posts': len(query)})
		return context


class ArticlesView(TemplateView):
	template_name = 'core/articles.html'

	def get_context_data(self, **kwargs):
		return {'articles': Article.objects.all()}


class ArticleDetailView(DetailView):
	template_name = 'core/article.html'
	model = Comment

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context


class ArticleView(CreateView):
	template_name = 'core/article.html'
	form_class = CommentForm
	model = Article
	success_url = ''
	slug_field = 'slug'

	def get_context_data(self, **kwargs):
		art = self.get_object()
		comments = Comment.find_by_art(art)
		ctx = {'article': art, 'comments': comments}
		return ctx

	def form_valid(self, form):
		comment = form.save(commit=False)
		comment.article = Article.find_by_slug(self.get_object().slug)
		comment.username = str(self.request.user)
		# do something here
		comment.save()
		return render(self.request, self.template_name, self.get_context_data())


def article_view(request, article_slug):
	art = Article.find_by_slug(article_slug)
	comments = Comment.find_by_art(art)
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.article = Article.find_by_slug(article_slug)
			comment.username = str(request.user)
			# do something here
			comment.save()
	if art:
		ctx = {'article': art, 'comments': comments}
		return render(request, 'core/article.html', ctx)
	else:
		return render(request, 'core/error404.html')
