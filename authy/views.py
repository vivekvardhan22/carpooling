from django.shortcuts import render, redirect, get_object_or_404
from authy.forms import SignupForm, ChangePasswordForm, EditProfileForm
from django.contrib.auth.models import User
from post.models import Post, Stream
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.db import transaction 
from authy.models import Profile
from django.template import loader
from django.http import HttpResponse

from django.core.paginator import Paginator

from django.urls import resolve

import uuid
from django.contrib import messages

# Create your views here.
def UserProfile(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)
	url_name = resolve(request.path).url_name

	if url_name == 'profile':
		posts = Post.objects.filter(user=user).order_by('-posted')

	else:
		posts = profile.favorites.all()
	
	posts_count = Post.objects.filter(user=user).count()

	#Pagination
	paginator = Paginator(posts, 6)
	page_number = request.GET.get('page')
	posts_paginator = paginator.get_page(page_number)

	template = loader.get_template('profile.html')

	context = {
		'posts': posts_paginator,
		'profile':profile,
		'posts_count':posts_count,
		'url_name':url_name,
	}

	return HttpResponse(template.render(context, request))


def Signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)  # Note the request.FILES here
        if form.is_valid():
            with transaction.atomic():
                # Create the base user
                user = User.objects.create_user(
                    username=form.cleaned_data.get('username'),
                    email=form.cleaned_data.get('email'),
                    password=form.cleaned_data.get('password')
                )
                
                # Get the automatically created profile
                profile = Profile.objects.get(user=user)
                
                # Update profile fields
                profile.first_name = form.cleaned_data.get('first_name')
                profile.last_name = form.cleaned_data.get('last_name')
                profile.profile_info = form.cleaned_data.get('profile_info')
                
                # Handle the picture upload
                picture = request.FILES.get('picture')
                if picture:
                    profile.picture = picture
                
                profile.save()

            return redirect('index')
    else:
        form = SignupForm()
    
    context = {
        'form': form,
    }

    return render(request, 'signup.html', context)



@login_required
def EditProfile(request):
	user = request.user.id
	profile = Profile.objects.get(user__id=user)

	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES)
		if form.is_valid():
			profile.picture = form.cleaned_data.get('picture')
			profile.first_name = form.cleaned_data.get('first_name')
			profile.last_name = form.cleaned_data.get('last_name')
			profile.location = form.cleaned_data.get('location')
			profile.profile_info = form.cleaned_data.get('profile_info')
			profile.save()
			return redirect('index')
	else:
		form = EditProfileForm()

	context = {
		'form':form,
	}

	return render(request, 'edit_profile.html', context)




