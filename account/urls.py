from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
  path('',views.index, name='index'),
  path('about/', views.about, name='about'),
  path('signup/', views.signup, name='signup'),
  path('login/', views.loginuser, name='login'),
  path('logout/', views.logoutuser, name='logout'),

  path('profile/<str:pk>/', views.profile, name='profile'),
  path('profile_form/<str:pk>/', views.edit_profile, name='profile_form'),

  # path('search_profiles/<str:search_query>/', views.search_profiles, name='search_profiles'),
  path('search_profiles/', views.search_profiles, name='search_profiles'),

  path('send_friend_request/<str:sender_id>/<str:receiver_id>/', views.send_frnd_req, name='send_friend_request'),
  path('delete_friend_request/<str:sender_id>/<str:receiver_id>/', views.delete_frnd_req, name='delete_friend_request'),
  path('cancel_friend_request/<str:sender_id>/<str:receiver_id>/', views.cancel_frnd_req, name='cancel_friend_request'),
  path('accept_friend_request/<str:sender_id>/<str:receiver_id>/', views.accept_frnd_req, name='accept_friend_request'),

  path('friends/', views.view_friends, name='friends'),
  path('remove_from_friend_list/<str:friend_id>/', views.remove_from_friend_list, name='remove_from_friend_list'),

  path('notifications/', views.notifications, name='notifications'),

  path('start_or_join_chat/<str:profile_id>/', views.start_or_join_chat, name='start_or_join_chat'),
  path('inbox/<str:room_name>/', views.inbox, name='inbox'),
  path('messages/', views.messages, name='messages'),
  
]
