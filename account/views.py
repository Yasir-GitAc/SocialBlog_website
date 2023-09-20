from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib import messages as django_messages
from .models import Profile, Notifications, Room, Message
from post.models import Post
from .forms import custom_user_creation_form, profile_form
import uuid
# Create your views here.

def index(request):
  search_query = ''

  if request.GET.get('search_query'):
    search_query = request.GET.get('search_query')


    posts = Post.objects.filter(
      Q(post_content__icontains = search_query)|
      Q(owner__name__icontains=search_query)
    )

    context = {
      'posts': posts,
      'search_query': search_query
    }
    return render(request, 'list_item.html', context)
  else:
    posts = Post.objects.all().order_by('-created')

    first_two_posts = posts[:2]
    second_two_posts = posts[2:4]
    third_two_posts = posts[4:6]
    fourth_two_posts = posts[6:8]

    if request.user.is_authenticated:
      friends_list = list(request.user.profile.friends.all())
    else:
      friends_list = []

    
    context = {
      'posts': posts,
      'first_two_posts': first_two_posts,
      'second_two_posts': second_two_posts,
      'third_two_posts': third_two_posts,
      'fourth_two_posts': fourth_two_posts,
      'contact_list': friends_list,
    }
    return render(request, 'index.html', context)


def search_profiles(request):
  query = ''
  if request.GET.get('query'):
    query = request.GET.get('query')

  profiles = Profile.objects.filter(
    Q(name__icontains = query)|
    Q(bio__icontains = query)|
    Q(contact__icontains = query)|
    Q(work__icontains = query)|
    Q(location__icontains = query)|
    Q(username__icontains = query)|
    Q(email__icontains = query)
  )

  context = {
    'profiles':profiles,
    'query': query,
  }

  return render(request, 'account/profile_list.html', context)


def about(request):
  admin_profile = Profile.objects.get(id='c850f805-2cd2-4013-9436-78be4f9d95d9')
  print(admin_profile)
  context = {
    'admin':admin_profile,
  }
  return render(request, 'about.html', context)

def loginuser(request):
  if request.user.is_authenticated:
    django_messages.info('your are already logged in')
    return redirect('account:index')

  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      django_messages.success(request, 'LogIn Successful'+ ' ' +username)
      return redirect('account:index')
    else:
      print('Credentials is not matching, please try again.')
      django_messages.error(request, 'Credentials do not match, please try again.')
      return redirect('account:login')

  return render(request, 'account/login.html')


@login_required(login_url='account:login')
def logoutuser(request):
  logout(request)
  django_messages.success(request, 'Successfully Logged Out')
  return redirect('account:index')


def signup(request):
  form = custom_user_creation_form()

  if request.user.is_authenticated:
    return redirect('account:index')
  
  if request.method == 'POST':
    form = custom_user_creation_form(request.POST)
    if form.is_valid():
      form.save()

      username = form.cleaned_data['username']
      password = form.cleaned_data['password1']
      user = authenticate(request, username=username, password=password)

      if user is not None:
        login(request, user)
        django_messages.success(request, 'SignUp Successful')
        # return redirect('account:edit_profile', pk=user.profile_set.id)
        return redirect('account:index')
      else:
        django_messages.error(request, 'An error occured during signup, please try again')
        return redirect('account:signup')
      
  context = {
    'form':form
  }
  return render(request, 'account/signup.html', context)


# @login_required(login_url='account:login')
def profile(request,pk):
  profile = Profile.objects.get(id=pk)
  posts = profile.post_set.all().order_by('-created')
  
  if request.user.is_authenticated:
    friends = list(request.user.profile.friends.all())
    friend_requests = list(request.user.profile.friend_request.all())
  else:
    friends = []
    friend_requests = []

  context = {
    'profile':profile,
    'posts' : posts,
    'friends':friends,
    'friend_requests': friend_requests,
  }

  print(friend_requests)
  return render(request, 'account/profile.html', context)



@login_required(login_url='account:login')
def edit_profile(request,pk):
  profile = Profile.objects.get(id=pk)
  form = profile_form(instance = profile)

  if request.method == 'POST':
    form = profile_form(request.POST, request.FILES, instance=profile)

    if form.is_valid():
      form.save()
      print('profile updated')
      django_messages.success(request, 'Profile Updated')

      return redirect('account:profile', pk=pk)
  
  context = {
    'form':form
  }

  return render(request, 'account/profile_form.html', context)


@login_required(login_url='account:login')
def notifications(request):
  notification_list = Notifications.objects.filter(receivers = request.user.profile)

  print(notification_list)

  for notification in notification_list:
    notification.seen = True
    notification.save()

  context = {
    'notification_list':notification_list,
  }
  return render(request, 'account/notifications.html', context)


@login_required(login_url='account:login')
def send_frnd_req(request, sender_id, receiver_id):
  sender = Profile.objects.get(id=sender_id)
  receiver = Profile.objects.get(id=receiver_id)
  sender_name = sender.name
  subject = f"{sender_name} sent you friend request"

  
  notification = Notifications.objects.create(
    type = 'friend_request_send',
    subject = subject,
    sender = sender,
  )
  notification.receivers.set([receiver])
  
  sender.friend_request.add(receiver)
  print('friend request was sent')

  return redirect('account:profile', pk=receiver_id)
  

@login_required(login_url='account:login')
def delete_frnd_req(request, sender_id, receiver_id):
  sender = Profile.objects.get(id=sender_id)
  receiver = Profile.objects.get(id=receiver_id)
  notification_of_req = Notifications.objects.filter(sender=sender, receivers=receiver).first()

  # Convert the ManyToMany manager to a list
  friend_requests = list(sender.friend_request.all())

  if receiver in friend_requests:
    print(f"This profile {receiver} is in sender's friend request. Deleting it now.")
    print('Deleting now')
    sender.friend_request.remove(receiver)

    if notification_of_req:
      notification_of_req.delete()
  else:
    print('Receiver not found in sender\'s friend request.')

  print('Delete function worked')

  return redirect('account:profile', pk=receiver_id)


@login_required(login_url='account:login')
def cancel_frnd_req(request, sender_id, receiver_id):
  profile_to_remove = Profile.objects.get(id=receiver_id)
  frnd_req_sender = Profile.objects.get(id=sender_id)
  notification_of_req = Notifications.objects.filter(sender=frnd_req_sender, receivers=profile_to_remove).first()

  #frnd_req list from which this profile is to be removed
  frnd_req_sender.friend_request.remove(profile_to_remove)

  if notification_of_req:
    notification_of_req.delete()

  print('frnd_req_canceled')
  messages.error(request, 'friend request canceled')

  return redirect('account:notifications')
  
@login_required(login_url='account:login')
def accept_frnd_req(request, sender_id, receiver_id):
  profile_that_will_accept = Profile.objects.get(id=receiver_id)
  profile_that_send_req = Profile.objects.get(id=sender_id)
  notification_of_req = Notifications.objects.filter(sender=profile_that_send_req, receivers=profile_that_will_accept).first()

  profile_that_will_accept.friends.add(profile_that_send_req)

  notification_of_accept = Notifications.objects.create(
    type = 'friend_request_accept',
    subject = f"{profile_that_will_accept.name} accepted your friend request",
    sender = profile_that_will_accept,
  )
  notification_of_accept.receivers.set([profile_that_send_req])

  if notification_of_req:
    notification_of_req.delete()

  return redirect('account:profile', pk=sender_id)


def view_friends(request):
  if request.user.is_authenticated:
    friends_list = list(request.user.profile.friends.all())
  else:
    friends_list = []
   
  profile_list = list(Profile.objects.all())

  contributor_profiles = []
  
  for profile in profile_list:
    if profile.post_set.count() > 2 :
      contributor_profiles.append(profile)

  context = {
    'friends_list': friends_list,
    'contributor_profiles': contributor_profiles,
  }
  return render(request, 'account/friends.html', context)


@login_required(login_url='account:login')
def remove_from_friend_list(request, friend_id):
  user_profile = Profile.objects.get(id=request.user.profile.id)
  profile_to_remove = Profile.objects.get(id=friend_id)

  print(user_profile)
  print(list(user_profile.friends.all()))

  user_profile.friends.remove(profile_to_remove)

  print(list(user_profile.friends.all()))

  return redirect('account:friends')


@login_required(login_url='account:login')
def start_or_join_chat(request, profile_id):
  user_profile = request.user.profile
  target_profile = Profile.objects.get(id=profile_id)

  #checking if any room consisting those user exist
  existing_rooms = Room.objects.filter(participants = user_profile).filter(participants = target_profile)
  print(existing_rooms)

  if existing_rooms.exists():
    existing_room = existing_rooms.first()
    print(existing_room)
    return redirect('account:inbox', room_name = existing_room.name)
  else:
    new_room = Room.objects.create(name = f"room_{uuid.uuid4().hex}")
    new_room.participants.add(user_profile, target_profile)
    print(new_room.name)
    return redirect('account:inbox', room_name=new_room.name)


@login_required(login_url='account:login')
def inbox(request, room_name):
  chat_room = Room.objects.get(name=room_name)
  messages = chat_room.message_set.all()
  participants_of_room = chat_room.participants.all()

  # for inbox messages list
  user_rooms = Room.objects.filter(participants = request.user.profile)
 
  for participant in participants_of_room:
    if participant == request.user.profile:
      sender_p = participant
    else:
      receiver_p = participant

  for message in messages:
    message.seen = True
    message.save()

  context = {
    'room' : chat_room,
    'messages': messages,
    'sender_participant': sender_p,
    'receiver_participant': receiver_p,
    'user_rooms': user_rooms,
  }

  return render(request, 'account/room.html', context)


@login_required(login_url='account:login')
def messages(request):
  user_rooms = Room.objects.filter(participants = request.user.profile)
 
  context = {
    'user_rooms': user_rooms,
  }

  return render(request, 'account/messages.html', context)
