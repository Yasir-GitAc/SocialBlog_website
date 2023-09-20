from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from account.models import Profile, Notifications
from .models import Post

def send_new_post_notification(sender, instance, created, **kwargs):
  if created :
    post = instance
    friends = list(post.owner.friends.all())

    notification = Notifications.objects.create(
      type = 'new_post_notification',
      subject = f'your friend {post.owner.name} made a new post,click to go to profile',
      sender = post.owner,
    )
    notification.receivers.set(friends)

    print('new post notification created')


post_save.connect(send_new_post_notification, sender=Post)