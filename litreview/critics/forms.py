from django import forms
from critics.models import Ticket, Review
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
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
        labels = {'headline': 'Titre',
                  'body': 'Commentaires',
                  'rating': 'Note'}
        rating_choices = [('0', 0), ('1', 1), ('2', 2),
                          ('3', 3), ('4', 4), ('5', 5)]
        widgets = {'rating': forms.RadioSelect(choices=rating_choices)}


class FollowUsersForm(forms.Form):
    user_to_follow = forms.CharField(
        max_length=20,
        label="Utilisateur à suivre",
        widget=forms.TextInput(attrs={"placeholder": "Nom d'utilisateur"})
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.followed_users = kwargs.pop('followed_users', None)
        self.user_to_follow = kwargs.pop('users_to_follow', None)
        super(FollowUsersForm, self).__init__(*args, **kwargs)

    def clean_user_to_follow(self):
        username = self.cleaned_data.get("user_to_follow")

        if username == str(self.user):
            raise ValidationError("Vous ne pouvez pas vous suivre vous-même !")
        elif username in [str(
                followed.followed_user) for followed in self.followed_users]:
            raise ValidationError(f"Vous êtes déjà abonné à {username}")
        elif username not in str(User.objects.all()):
            raise ValidationError(
                f"{username} n'est pas un utilisateur du site !")
        else:
            user = get_object_or_404(self.user_to_follow, username=username)
        return user
