from django.contrib import admin
from .models import Profile, Notifications, Room, Message

# Register your models here.


admin.site.register(Profile)
admin.site.register(Notifications)
admin.site.register(Room)
admin.site.register(Message)