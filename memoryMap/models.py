from django.conf import settings
from django.db import models
from django.db import models
from django.urls import reverse


# Create your models here.

class MarkedPlaces(models.Model):
    places_name = models.CharField(max_length=100)
    about_place = models.CharField(max_length=10000)
    x_location = models.FloatField()
    y_location = models.FloatField()
    user = models.ForeignKey('Users', default=None, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.places_name

    def get_absolute_url(self):
        return reverse('editMemory', kwargs={'mark_id', self.pk})

class Users(models.Model):
    vk_id = models.CharField(max_length=1000)


