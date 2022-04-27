from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from critics.models import Ticket
from critics.forms import TicketForm

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

def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            new_ticket = form.save()
            return redirect('flux-detail', new_ticket.id)

    else:
        form = TicketForm()

    return render(request,
                  'critics/ticket_create.html',
                  {'form': form})

def ticket_update(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('flux-detail', ticket.id)
    else:
        form = TicketForm(instance=ticket)

    return render(request, 'critics/ticket_modify.html', {'form': form})

def ticket_delete(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    if request.method == 'POST':
        ticket.delete()
        return redirect('posts')

    return render(request, 'critics/ticket_delete.html', {'ticket': ticket})

def create_critic(request):
    return render(request, 'critics/create_critic.html')

def answer_critic(request):
    return render(request, 'critics/answer_critic.html', {'demand':request.GET.get('demand')})

def posts(request):
    tickets = Ticket.objects.all()
    return render(request, 'critics/posts.html', {'tickets': tickets})

def modify_critic(request):
    return render(request, 'critics/modify_critic.html', {'demand':request.GET.get('demand')})


