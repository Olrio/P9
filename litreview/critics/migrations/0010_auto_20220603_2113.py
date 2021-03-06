# Generated by Django 4.0.4 on 2022-06-03 21:13

from django.db import migrations
from PIL import Image


def resize_image(apps, scheme_editor):
    Ticket = apps.get_model('critics', 'Ticket')
    for ticket in Ticket.objects.all():
        if ticket.image:
            image = Image.open(ticket.image)
            image.thumbnail((200, 200))
            image.save(ticket.image.path)


class Migration(migrations.Migration):

    dependencies = [
        ('critics', '0009_alter_userfollows_unique_together'),
    ]

    operations = [
        migrations.RunPython(resize_image)
    ]
