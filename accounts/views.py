from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import LoginForm, SignUpForm, EditForm, ProfileEditForm
from django.http import HttpResponse
# Create your views here.


def edit(request):
    """
    A simple function which edit or update user's profile.

    """
    if bool(Profile.objects.filter(user=request.user)) is False:
        obj = Profile(user=request.user)
        obj.save()
    if request.method == 'POST':
        user_form = EditForm(instance=request.user,
                             data=request.POST)
        profile_form = ProfileEditForm(
            files=request.FILES, instance=request.user.profile,
            data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            print('---------------------------------------')
            print(profile_form.cleaned_data['photo'])
            print('---------------------------------------')
            profile_form.save()
            messages.success(request, 'Your profile updated successfully')
            return redirect('blogposts:user_post_list', request.user.username, request.user.id)
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = EditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'accounts/edit.html', {
                      'user_form': user_form, 'profile_form': profile_form
                  })


def user_signup(request):
    """
    A  function which helps to signup new user.

    """
    if request.method == "POST":
        user_form = SignUpForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile(user=new_user)
            profile.save()

            # return HttpResponse('Your accounts is created')
            return redirect('blogposts:list')
    user_form = SignUpForm()
    return render(request, 'accounts/signup.html', {'user_form': user_form})


def user_login(request):
    """
    A simple function which helps to login user to their respective account.

    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            user = authenticate(request, username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # return HttpResponse('Authenticated Successfully')
                    return redirect('blogposts:user_post_list', request.user.username, request.user.id)
            else:
                return redirect('accounts:login')

    form = LoginForm()
    if request.user.is_authenticated:
        return redirect('accounts:edit')
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('accounts:login')
