from django import forms

from critics.models import Ticket, Review, UserFollows
from authentication.models import User



class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ['user']
        labels = {'title': 'Titre'}

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ['user', 'ticket']
        labels = {'headline': 'Titre', 'body': 'Commentaire', 'rating': 'Note'}
        rating_choices = [('0', 0), ('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)]
        widgets = {'rating': forms.RadioSelect(choices=rating_choices)}

class FollowUsersForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ['followed_user']



