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
from django.urls import path
import critics.views
import authentication.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentication.views.login_page, name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('register/', critics.views.register),
    path('flux/', critics.views.flux, name='flux'),
    path('flux/<int:id>/', critics.views.flux_detail, name='flux-detail'),
    path('subscribe/', critics.views.subscribe),
    path('ticket/create/', critics.views.ticket_create, name='ticket-create'),
    path('ticket/<int:id>/change/', critics.views.ticket_update, name='ticket-update'),
    path('ticket/<int:id>/delete/', critics.views.ticket_delete, name='ticket-delete'),
    path('create_critic/', critics.views.create_critic),
    path('answer_critic/', critics.views.answer_critic),
    path('posts/', critics.views.posts, name='posts'),
    path('modify_critic/', critics.views.modify_critic),
]
