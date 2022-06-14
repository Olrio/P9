from django.http import HttpResponse
from django.views.generic import View
from itertools import chain
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F, ExpressionWrapper, CharField
from django.core.paginator import Paginator
from critics.models import Ticket, Review, UserFollows
from critics.forms import TicketForm, ReviewForm, FollowUsersForm
from authentication.models import User
from django.core.exceptions import ValidationError
import datetime

@login_required()
def flux(request):
    reviews = Review.objects.filter(
        Q(user__in=[follow.followed_user for follow in UserFollows.objects.filter(user=request.user)]) |
        Q(user=request.user) |
        Q(ticket__user=request.user)
    )

    '''
        a queryset of all reviews whose author is not its ticket author
        such a queryset is needed to know if a review is possible on an autoreview
        if the ticket of the autoreview is present in this queryset, review on this ticket would be disable
        '''
    reviews_not_autoreview = Review.objects.filter(
        Q(user__in=[follow.followed_user for follow in UserFollows.objects.filter(user=request.user)]) |
        Q(user=request.user) |
        Q(ticket__user=request.user)).exclude(Q(user=F("ticket__user")))

    '''
    a queryset of all autoreviews, i.e. review an dticket have the same author
    '''
    autoreviews = Review.objects.filter(
        Q(user__in=[follow.followed_user for follow in UserFollows.objects.filter(user=request.user)]) |
        Q(user=request.user) |
        Q(ticket__user=request.user)).filter(Q(user=F("ticket__user")))


    tickets = Ticket.objects.filter(
        Q(user__in=[follow.followed_user for follow in UserFollows.objects.filter(user=request.user)]) |
        Q(user=request.user)).exclude(Q(id__in=[review.ticket.id for review in autoreviews]))

    reviewable_tickets =  Ticket.objects.filter(
        Q(user__in=[follow.followed_user for follow in UserFollows.objects.filter(user=request.user)]) | Q(user=request.user)).exclude(
        Q(id__in=[review.ticket.id for review in reviews_not_autoreview]))


    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda instance:instance.time_created,
        reverse=True
    )

    paginator = Paginator(tickets_and_reviews, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'reviewable': list(reviewable_tickets)
    }

    return render(request, 'critics/flux.html', context=context)


@login_required()
def subscribe(request):
    followed_users = UserFollows.objects.filter(user=request.user)
    followers = UserFollows.objects.filter(followed_user=request.user)
    users_to_follow = User.objects.all().exclude(
         Q(username__in=[follow.followed_user for follow in followed_users])| Q(username=request.user.username))
    if request.method == 'POST':
        form = FollowUsersForm(request.POST, user=request.user, followed_users=followed_users, users_to_follow=users_to_follow)
        if form.is_valid():
            new_follow = UserFollows()
            new_follow.followed_user = form.cleaned_data['user_to_follow']
            new_follow.user = request.user
            new_follow.save()
            return redirect('subscribe')
    else:
        form = FollowUsersForm()
    return render(request, 'critics/subscribe.html', context={'form': form,
                                                              'followed_users': list(followed_users),
                                                              'followers': list(followers)})

@login_required()
def unsubscribe(request, id):
    follow = get_object_or_404(UserFollows, id=id)
    if request.method == 'POST':
        follow.delete()
        return redirect('subscribe')
    return render(request, 'critics/unsubscribe.html', {'follow': follow})


@login_required()
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            new_ticket = form.save(commit=False)
            new_ticket.user = request.user
            new_ticket.save()
            return redirect('ticket-read', new_ticket.id)

    else:
        form = TicketForm()

    return render(request,
                  'critics/ticket_create.html',
                  {'form': form})

@login_required()
def ticket_read(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    return render(request, 'critics/ticket_read.html',
                  {'ticket': ticket})

@login_required()
def ticket_update(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.time_created = datetime.datetime.now()
            ticket.save()
            return render(request,
                          'critics/ticket_read.html', {"ticket":ticket})
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'critics/ticket_update.html', {'form': form})

@login_required()
def ticket_delete(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    if request.method == 'POST':
        ticket.delete()
        return redirect('posts')
    return render(request, 'critics/ticket_delete.html', {'ticket': ticket})


@login_required()
def review_create(request):
    ticket_form = TicketForm()
    review_form = ReviewForm()
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if all([ticket_form.is_valid(),review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return render(request, 'critics/review_read.html', {'ticket': ticket, 'review': review})
    return render(request,
                  'critics/review_create.html',
                  {'ticket_form': ticket_form,
                   'review_form': review_form})

@login_required()
def review_read(request, id):
    review = get_object_or_404(Review, id=id)
    return render(request, 'critics/review_read.html',
                  {'review': review})

@login_required()
def review_update(request, id):
    review = get_object_or_404(Review, id=id)
    ticket = get_object_or_404(Ticket, id=review.ticket.id)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST, request.FILES, instance=review)
        ticket_form = TicketForm(request.POST, request.FILES, instance=ticket)
        if all([ticket_form.is_valid(),review_form.is_valid()]):
            ticket_form.save()
            review = review_form.save(commit=False)
            review.time_created = datetime.datetime.now()
            review.save()
            return render(request,
                          'critics/review_read.html', {"review":review})
    else:
        review_form = ReviewForm(instance=review)
        ticket_form = TicketForm(instance=ticket)
    return render(request, 'critics/review_update.html', {'review_form': review_form,
                                                          'ticket_form': ticket_form})

@login_required()
def review_delete(request, id):
    review = get_object_or_404(Review, id=id)
    ticket = get_object_or_404(Ticket, id=review.ticket.id)
    if request.method == 'POST':
        review.delete()
        ticket.delete()
        return redirect('posts')
    return render(request, 'critics/review_delete.html', {'review': review})

@login_required()
def review_answer_ticket(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    review_form = ReviewForm()
    if request.method == 'POST':
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return render(request, 'critics/review_read.html', {'ticket': ticket, 'review': review})
    return render(request,
                  'critics/review_answer_ticket.html',
                  {'review_form': review_form,
                   'ticket': ticket})

@login_required()
def posts(request):
    reviews = Review.objects.filter(user=request.user)
    tickets = Ticket.objects.filter(user=request.user).exclude(id__in=[review.ticket.id for review in reviews])
    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )
    context = {'tickets_and_reviews': tickets_and_reviews,
               }
    return render(request, 'critics/posts.html', context=context)




