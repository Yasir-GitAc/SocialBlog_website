from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


def create_profile(sender, instance, created, **kwargs):
  if created :
    user = instance
    profile = Profile.objects.create(
      user = user,
      username = user.username,
      email = user.email
    )
    print('profile created')

    subject = 'Welcome to Devsearch'
    message = 'We are glad you are here'

    send_mail(
      subject,
      message,
      settings.EMAIL_HOST_USER,
      [profile.email],
      fail_silently=False,
    )


post_save.connect(create_profile, sender=User)