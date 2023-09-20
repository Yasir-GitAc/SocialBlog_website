import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Profile, Room, Message

class ChatConsumer(WebsocketConsumer):
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.room_name = None
    self.inbox = None
    self.room = None
    self.user = None

  def connect(self):
    self.room_name = self.scope['url_route']['kwargs']['room_name']
    self.inbox = self.room_name
    self.room = Room.objects.get(name=self.room_name)
    
    user = self.scope['user']
    self.user = Profile.objects.get(user=user)

    self.accept()

    async_to_sync(self.channel_layer.group_add)(
      self.inbox,
      self.channel_name,
    )

    async_to_sync(self.channel_layer.group_send)(
      self.inbox,
      {
        'type': 'user_join',
        'message': f'{self.user.name} has joined chat'
      }
    )

    # self.send(json.dumps({
    #   'type': 'user_join',
    #   'message': f'{self.user.name} is active now',
    # }))
    
    self.room.online.add(self.user)

  
  def disconnect(self, code):
    async_to_sync(self.channel_layer.group_discard)(
      self.inbox,
      self.channel_name,
    )

    self.send(json.dumps({
      'type': 'user_leave',
      'message': f'{self.user.username} has left'
    }))

    self.room.online.remove(self.user)


  def receive(self, text_data=None, bytes_data=None):
    text_data_json = json.loads(text_data)
    message = text_data_json['message']

    async_to_sync(self.channel_layer.group_send)(
      self.inbox,
      {
        'type': 'chat_message',
        'message': message,
      }
    )
    Message.objects.create(writer=self.user, room=self.room, content=message)

  def chat_message(self, event):
    self.send(text_data=json.dumps(event))

  def user_join(self, event):
    self.send(text_data=json.dumps(event))

  def user_leave(self, event):
    self.send(text_data=json.dumps(event))

