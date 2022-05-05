import django.contrib.auth.forms
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import View
from django.conf import settings
from authentication.forms import RegisterForm

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


#
# def logout_user(request):
#     logout(request)
#     return redirect('login')

# def login_page(request):
#     form = LoginForm()
#     message = ''
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             user = authenticate(
#                 username=form.cleaned_data['username'],
#                 password=form.cleaned_data['password'],
#             )
#             if user is not None:
#                 login(request, user)
#                 return redirect('flux')
#             else:
#                 message = 'Identifiants invalides'
#     return render(request,
#                   'authentication/login.html',
#                   context={'form': form,
#                            'message': message})
