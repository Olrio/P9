from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from critics.models import Ticket

def login(request):
    return render(request, 'critics/login.html')

def register(request):
    return render(request, 'critics/register.html')

def flux(request):
    tickets = Ticket.objects.all()
    return render(request, 'critics/flux.html', {'tickets': tickets})

def flux_detail(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    return render(request, 'critics/flux_detail.html',
                  {'ticket': ticket})

def subscribe(request):
    return render(request, 'critics/subscribe.html')

def ticket(request):
    return render(request, 'critics/ticket.html')

def create_critic(request):
    return render(request, 'critics/create_critic.html')

def answer_critic(request):
    return render(request, 'critics/answer_critic.html', {'demand':request.GET.get('demand')})

def posts(request):
    return render(request, 'critics/posts.html')

def modify_critic(request):
    return render(request, 'critics/modify_critic.html', {'demand':request.GET.get('demand')})

def modify_ticket(request):
    return render(request, 'critics/modify_ticket.html', {'demand':request.GET.get('demand')})
