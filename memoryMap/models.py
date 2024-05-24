from django.conf import settings
from django.db import models
from django.db import models
from django.urls import reverse


# Create your models here.

class MarkedPlaces(models.Model):
    places_name = models.CharField(max_length=40, verbose_name='Название места')
    about_place = models.CharField(max_length=10000, verbose_name='О месте')
    x_location = models.FloatField()
    y_location = models.FloatField()
    user = models.ForeignKey('Users', default=None, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.places_name


class Users(models.Model):
    vk_id = models.CharField(max_length=1000, verbose_name='id зашедшего пользователя в вк')


