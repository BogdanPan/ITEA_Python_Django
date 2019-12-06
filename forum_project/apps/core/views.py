from django.shortcuts import render
from .models import Article, Comment
from ..core.forms import CommentForm, ArticleForm
from django.views.generic import View, TemplateView, ListView, DetailView, RedirectView, CreateView
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class MainPageView(CreateView):
	template_name = 'core/main_page.html'
	form_class = ArticleForm
	model = Article
	success_url = ''

	def get_context_data(self, **kwargs):
		query = Article.objects.all().order_by('-created')[:5]
		context = ({'articles': query, 'number_of_posts': len(query), 'form':self.form_class})
		return context

	def form_valid(self, form):
		form.save()
		return render(self.request, self.template_name, self.get_context_data())

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
		paginator = Paginator(object_list=comments.order_by('-created'), per_page=5)
		page = self.request.GET.get('page')
		try:
			comments = paginator.page(page)
		except PageNotAnInteger:
			comments = paginator.page(1)
		except EmptyPage:
			comments = paginator.page(paginator.num_pages)

		ctx = {'article': art, 'comments': comments}
		return ctx

	def form_valid(self, form):
		comment = form.save(commit=False)
		comment.article = Article.find_by_slug(self.get_object().slug)
		comment.user = self.request.user
		# do something here
		comment.save()
		return render(self.request, self.template_name, self.get_context_data())
