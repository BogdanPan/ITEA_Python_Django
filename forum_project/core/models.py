from django.db import models
from django.utils.text import slugify
# Create your models here.


class Article(models.Model):
	title = models.TextField(max_length=255)
	text = models.TextField()
	image = models.ImageField(upload_to='article_images', blank=True, null=True)
	slug = models.SlugField(default='', blank=True)

	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	@classmethod
	def find_by_slug(cls, slug):
		return cls.objects.filter(slug=slug).first()

	@classmethod
	def get_all_url_names(cls):
		name_list = []
		for obj in cls.objects.all():
			name_list.append(obj.name)
		return name_list

	def main_page_text(self):
		full_text_str = self.text
		full_text_str_len = len(full_text_str)
		if full_text_str_len <= 270:
			return full_text_str[:full_text_str_len]
		else:
			return full_text_str[:270]+'...'

	def __str__(self):
		return f"{self.title}, {self.title}"

	def save(self, *args, **kwargs):
		self.slug = slugify(value=self.title, allow_unicode=True)
		super().save()
