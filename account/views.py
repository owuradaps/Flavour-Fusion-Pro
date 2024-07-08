

from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from recipe.models import Recipe
from .models import UserProfile


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created successfully for {user.username}!')
            return redirect('account:profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}! You have successfully logged in.")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html', {"form": form})
    
@login_required
def profile(request, username=None):
    if username:
        profile_user = get_object_or_404(User, username=username)
    else:
        profile_user = request.user

    if request.method == 'POST' and request.user == profile_user:
        u_form = UserUpdateForm(request.POST, instance=profile_user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('account:profile')
    else:
        u_form = UserUpdateForm(instance=profile_user)
        p_form = ProfileUpdateForm(instance=profile_user.profile)

    user_recipes_list = Recipe.objects.filter(user=profile_user).order_by('-created_at')
    paginator = Paginator(user_recipes_list, 6)
    page = request.GET.get('page')
    user_recipes = paginator.get_page(page)

    context = {
        'profile_user': profile_user,
        'u_form': u_form,
        'p_form': p_form,
        'user_recipes': user_recipes
    }
    return render(request, 'account/profile.html', context)

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.") 
    return redirect('home')

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    request.user.userprofile.followers.add(user_to_follow)
    return redirect('user_profile', username=username)

@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    request.user.userprofile.followers.remove(user_to_unfollow)
    return redirect('user_profile', username=username) 


def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    user_recipes = Recipe.objects.filter(user=profile_user)
    followers = profile_user.userprofile.followers.all()
    favorite_recipes = profile_user.userprofile.favorite_recipes.all()

    context = {
        'profile_user': profile_user,
        'user_recipes': user_recipes,
        'followers': followers,
        'favorite_recipes': favorite_recipes,
    }
    return render(request, 'account/user_profile.html', context)