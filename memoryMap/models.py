"""Models"""

from django.db import models

class MarkedPlaces(models.Model):
    """
    Model which stores impressions/memories
    """
    places_name = models.CharField(max_length=40, verbose_name='Название места')
    about_place = models.CharField(max_length=10000, verbose_name='О месте')
    x_location = models.FloatField()
    y_location = models.FloatField()
    user = models.ForeignKey('Users', default=None, null=True, on_delete=models.CASCADE)

class Users(models.Model):
    """
    Model which stores users vk IDs
    """
    vk_id = models.CharField(max_length=1000,
                             verbose_name='id зашедшего пользователя в вк')
