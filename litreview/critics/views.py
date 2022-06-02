from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from critics.models import Ticket, Review, UserFollows
from critics.forms import TicketForm, ReviewForm, FollowUsersForm

@login_required()
def flux(request):
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    return render(request, 'critics/flux.html', {'tickets': tickets, 'reviews': reviews})

@login_required()
def flux_detail(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    return render(request, 'critics/flux_detail.html',
                  {'ticket': ticket})

@login_required()
def subscribe(request):
    form = FollowUsersForm(instance=request.user)
    follows = UserFollows.objects.filter(user=request.user)
    if request.method == 'POST':
        form = FollowUsersForm(request.POST, instance=request.user)
        if form.is_valid():
            new_follow = UserFollows()
            new_follow.followed_user = form.cleaned_data['followed_user']
            new_follow.user = request.user
            new_follow.save()
            return redirect('flux')
    return render(request, 'critics/subscribe.html', context={'form': form, 'follows': follows})

@login_required()
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            new_ticket = form.save(commit=False)
            new_ticket.user = request.user
            new_ticket.save()
            return redirect('flux-detail', new_ticket.id)

    else:
        form = TicketForm()

    return render(request,
                  'critics/ticket_create.html',
                  {'form': form})

@login_required()
def ticket_update(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return render(request,
                          'critics/flux_detail.html', {"ticket":ticket})
    else:
        form = TicketForm(instance=ticket)

    return render(request, 'critics/ticket_modify.html', {'form': form})

@login_required()
def ticket_delete(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    if request.method == 'POST':
        ticket.delete()
        return redirect('posts')

    return render(request, 'critics/ticket_delete.html', {'ticket': ticket})


@login_required()
def create_critic(request):
    ticket_form = TicketForm()
    critic_form = ReviewForm()
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        critic_form = ReviewForm(request.POST)
        if all([ticket_form.is_valid(),critic_form.is_valid()]):
            new_ticket = ticket_form.save(commit=False)
            new_ticket.user = request.user
            new_ticket.save()
            new_critic = critic_form.save(commit=False)
            new_critic.ticket = new_ticket
            new_critic.user = request.user
            new_critic.save()
            return render(request, 'critics/flux_detail.html', {'ticket': new_ticket, 'critic': new_critic})
    return render(request,
                  'critics/create_critic.html',
                  {'ticket_form': ticket_form,
                   'critic_form': critic_form})

@login_required()
def answer_critic(request):
    return render(request, 'critics/answer_critic.html', {'demand':request.GET.get('demand')})

@login_required()
def posts(request):
    tickets = Ticket.objects.all()
    return render(request, 'critics/posts.html', {'tickets': tickets})

@login_required()
def modify_critic(request):
    return render(request, 'critics/modify_critic.html', {'demand':request.GET.get('demand')})


