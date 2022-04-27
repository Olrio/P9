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
from critics import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('register/', views.register),
    path('flux/', views.flux, name='flux'),
    path('flux/<int:id>/', views.flux_detail, name='flux-detail'),
    path('subscribe/', views.subscribe),
    path('ticket/create/', views.ticket_create, name='ticket-create'),
    path('ticket/<int:id>/change/', views.ticket_update, name='ticket-update'),
    path('ticket/<int:id>/delete/', views.ticket_delete, name='ticket-delete'),
    path('create_critic/', views.create_critic),
    path('answer_critic/', views.answer_critic),
    path('posts/', views.posts, name='posts'),
    path('modify_critic/', views.modify_critic),
]
