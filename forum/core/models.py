from django.db import models

# Create your models here.


class Article(models.Model):
	name = models.CharField(max_length=30)
	article_name = models.TextField()
	article_text = models.TextField()
	article_image = models.ImageField(upload_to='article_images', blank=True)

	@classmethod
	def find_by_name(cls, name):
		return cls.objects.filter(name=name).first()

	@classmethod
	def get_all_url_names(cls):
		name_list = []
		for obj in cls.objects.all():
			name_list.append(obj.name)
		return name_list
