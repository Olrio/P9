from django.contrib import admin
from authentication.models import User
from critics.models import Ticket, Review, UserFollows

admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(User)
admin.site.register(UserFollows)