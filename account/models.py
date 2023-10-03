from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class Profile(models.Model):
  id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
  username = models.CharField(max_length=100, blank=True, null=True)
  name = models.CharField(max_length=200, blank=True, null=True)
  email = models.EmailField(max_length=500, blank=True, null=True)
  profile_picture = models.ImageField(upload_to ='profile_images', default= 'profile_images/user-default.jpg', blank=True, null=True)
  bio = models.TextField(max_length=350, null=True, blank=True)
  work = models.CharField(max_length=200,null=True, blank=True)
  location = models.CharField(max_length=200,null=True, blank=True)
  contact = models.CharField(max_length=200,null=True, blank=True)
  social_website = models.CharField(max_length=200,null=True, blank=True)
  facebook = models.CharField(max_length=200,null=True, blank=True)
  linkedin = models.CharField(max_length=200, null=True, blank=True)
  twitter = models.CharField(max_length=200, null=True, blank=True)
  you_tube = models.CharField(max_length=200, null=True, blank=True)
  friends = models.ManyToManyField('self', blank=True)
  friend_request = models.ManyToManyField('self', blank=True)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  def __str__(self):
    return str(self.name)
  
  class Meta:
    ordering =  ['created']


class Notifications(models.Model):
  id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
  type = models.CharField(max_length=200, blank=True, null=True)
  seen = models.BooleanField(default=False, blank=True)
  subject = models.CharField(max_length=200, blank=True, null=True)
  sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='notifications_sender', null=True, blank=True)
  receivers = models.ManyToManyField(Profile,related_name='notification_receiver', blank=True)
  created = models.DateTimeField(auto_now_add=True) 

  def __str__(self):
    return str(self.subject)
  
  class Meta:
    ordering =  ['-created']



class Room(models.Model):
  id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
  name = models.CharField(max_length=255, unique=True)
  created = models.DateTimeField(auto_now_add=True)
  participants = models.ManyToManyField('Profile', related_name='rooms', blank=True)
  online = models.ManyToManyField('Profile', blank=True)

  def __str__(self):
    return self.name


class Message(models.Model):
  writer = models.ForeignKey(Profile, on_delete=models.CASCADE)
  room = models.ForeignKey(Room, on_delete=models.CASCADE)
  content = models.CharField(max_length=512)
  seen = models.BooleanField(default=False, blank=True)
  created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.content
  
