import django.contrib.auth.forms
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import View
from django.conf import settings
from authentication.forms import RegisterForm, UploadProfilePhotoForm

class RegisterPageView(View):
    template_name = 'authentication/register.html'
    form_class = RegisterForm

    def get(self, request):
        form = self.form_class()
        return render(request,
                      self.template_name,
                      {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request,
                      self.template_name,
                      {'form': form})

class UploadProfilePhoto(LoginRequiredMixin, View):
    def get(self, request):
        self.form_class = UploadProfilePhotoForm(instance=request.user)
        return render(request,
                      'authentication/change_profile_photo.html',
                      context={'form':self.form_class})

    def post(self, request):
        self.form_class = UploadProfilePhotoForm(request.POST, request.FILES, instance=request.user)
        if self.form_class.is_valid():
            self.form_class.save()
            return redirect('flux')
        return render(request,
                      'authentication/change_profile_photo.html',
                      context={'form':self.form_class})