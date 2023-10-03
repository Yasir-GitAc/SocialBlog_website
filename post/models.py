from django.db import models
from account.models import Profile
import uuid
from django.utils import timezone
# Create your models here.

class Reply(models.Model):
  id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
  owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
  reply_content = models.TextField(max_length=200, null=True, blank=True)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)



class Comment(models.Model):
  id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
  owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
  comment_content = models.TextField(max_length=200, null=True, blank=True)
  reply = models.ForeignKey(Reply, on_delete=models.CASCADE, null=True, blank=True)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)


#new ui onojayi upvote and downvote bad, upvote r jaygay like

class Post(models.Model):
  id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
  owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
  post_content = models.TextField(max_length=2000, null=True, blank=True)
  post_img = models.ImageField(upload_to='uploaded_images', blank=True, null=True)
  upvote = models.IntegerField(null=True, blank=True)
  downvote = models.IntegerField(null=True, blank=True)
  comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  def __str__(self):
    return   self.post_content