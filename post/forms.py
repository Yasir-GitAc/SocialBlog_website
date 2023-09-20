from django.forms import ModelForm
from .models import Post, Comment, Reply

class post_form(ModelForm):
  class Meta:
    model = Post
    fields = ['post_content', 'post_img']

  def __init__(self, *arg, **kwargs):
    super(post_form, self).__init__(*arg, **kwargs)

    self.fields['post_content'].widget.attrs['placeholder'] = 'Write your post content, max-length 2000 characters'