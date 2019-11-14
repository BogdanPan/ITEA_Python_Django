from django import forms
from ..core.models import Comment, Article


class CommentForm(forms.ModelForm):
	text = forms.TextInput()

	class Meta(object):
		model = Comment
		fields = '__all__'

