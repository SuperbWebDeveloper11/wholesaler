from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from rest_framework.authtoken.views import ObtainAuthToken # for drf
from rest_framework.authtoken.models import Token # for drf
from rest_framework.response import Response # for drf
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'accounts/dashboard.html')


class Register(View):
    def post(self, request, *args, **kwargs):
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password']) # Set a hashed password 
            new_user.save()
            Profile.objects.create(user=new_user) # Create a blank profile for this user
            return render(request, 'accounts/register_done.html', {'new_user': new_user})
        else:
            return render(request, 'accounts/register.html', {'user_form': user_form})

    def get(self, request, *args, **kwargs):
        user_form = UserRegistrationForm()
        return render(request, 'accounts/register.html', {'user_form': user_form})


class EditProfile(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            messages.warning(request, 'Error updating your profile')
        return render(request, 'accounts/edit.html', {'user_form': user_form, 'profile_form': profile_form})

    def get(self, request, *args, **kwargs):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, 'accounts/edit.html', {'user_form': user_form, 'profile_form': profile_form})


# give a username and password and obtain new token each time
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        try: # delete and recreate token
            token = Token.objects.get(user=user)
            token.delete()
            token = Token.objects.create(user=user)
        except: # create new token
            token = Token.objects.create(user=user)

        return Response({ 'token': token.key, 'user_id': user.pk, 'email': user.email })

