from django.db import models
from autoslug import AutoSlugField


class Article(models.Model):
	title = models.TextField(max_length=255)
	text = models.TextField()
	image = models.ImageField(upload_to='Article_images', blank=True, null=True)
	slug = AutoSlugField(populate_from='title', null=True, unique=True, allow_unicode=True)

	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	@classmethod
	def find_by_slug(cls, slug):
		return cls.objects.filter(slug=slug).first()

	def get_number_of_comments(self):
		return len(Comment.find_by_art(self))

	def __str__(self):
		return f"{self.title}, {self.title}"

	def save(self, *args, **kwargs):
		self.slug = None
		super().save(*args, **kwargs)


class Comment(models.Model):
	article = models.ForeignKey(to=Article, on_delete=models.CASCADE, blank=True, null=True)
	username = models.CharField(max_length=255, blank=True, null=True)
	text = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	@classmethod
	def find_by_art(cls, article):
		return cls.objects.filter(article=article)
