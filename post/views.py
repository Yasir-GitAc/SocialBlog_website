from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from account.models import Profile, Notifications
from .models import Post, Comment, Reply
from .forms import post_form
# Create your views here.


@login_required(login_url='account:login')
def create_post(request):
  form = post_form()
  profile = request.user.profile

  if request.method == 'POST':
    form = post_form(request.POST, request.FILES)
    if form.is_valid():
      p_form = form.save(commit=False)
      p_form.owner = profile
      p_form.save()
      django_messages.success(request, 'post created successfully')

      return redirect('account:profile', pk=profile.id)

  context = {
    'form' : form
  }
  return render(request, 'post/post_form.html', context)


@login_required(login_url='account:login')
def edit_post(request, pk):
  post = Post.objects.get(id=pk)
  form = post_form(instance=post)
  if request.method == 'POST':
    form = post_form(request.POST, request.FILES, instance=post)
    if form.is_valid():
      form.save()
      django_messages.success(request, 'post updated')
      return redirect('account:profile', pk=request.user.profile.id)

  context = {
    'form':form
  }
  return render(request, 'post/post_form.html', context)


@login_required(login_url='account:login')
def delete_post(request, pk):
  profile_id = request.user.profile.id
  post = Post.objects.get(id=pk)
  post_owner = post.owner.id

  if profile_id != post_owner :
    return redirect('account:index')

  context = {
    'post':post,
  }

  return render(request, 'post/delete_post.html', context)

@login_required(login_url='account:login')
def confirm_delete(request, pk):
  profile_id = request.user.profile.id
  post = Post.objects.get(id=pk)
  post_owner = post.owner.id

  if profile_id == post_owner:
    post.delete()
    django_messages.warning(request, 'post deleted')
    return redirect('account:profile', pk=profile_id)
  else:
    return redirect('account:index')
