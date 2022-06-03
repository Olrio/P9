"""litreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
import critics.views
import authentication.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', LogoutView.as_view(
        template_name='authentication/logout.html'
    ), name='logout'),
    path('password_change/', PasswordChangeView.as_view(
        template_name='authentication/password_change.html',
        success_url='../password_change_done/'
    ), name='new_password'),
    path('password_change_done/', PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'
    ),
         name='password_changed'),
    path('register/', authentication.views.RegisterPageView.as_view(), name='register'),
    path('flux/', critics.views.flux, name='flux'),
    path('flux/<int:id>/', critics.views.flux_detail, name='flux-detail'),
    path('subscribe/', critics.views.subscribe, name='subscribe'),
    path('unsubscribe/<int:id>', critics.views.unsubscribe, name='unsubscribe'),
    path('ticket/create/', critics.views.ticket_create, name='ticket-create'),
    path('ticket/<int:id>/change/', critics.views.ticket_update, name='ticket-update'),
    path('ticket/<int:id>/delete/', critics.views.ticket_delete, name='ticket-delete'),
    path('critic/create/', critics.views.create_critic, name='critic-create'),
    path('critic/answer/', critics.views.answer_critic, name='critic-answer'),
    path('posts/', critics.views.posts, name='posts'),
    path('critic/change/', critics.views.modify_critic, name='critic-update'),
    path('profile_photo/', authentication.views.UploadProfilePhoto.as_view(), name='profile-photo'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
