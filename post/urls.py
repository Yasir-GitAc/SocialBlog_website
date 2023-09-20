from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
  path('create_post/', views.create_post, name='create_post'),
  path('edit_post/<str:pk>/', views.edit_post, name='edit_post'),
  path('delete_post/<str:pk>/', views.delete_post, name='delete_post'),
  path('confirm_delete/<str:pk>/', views.confirm_delete, name='confirm_delete'),
]