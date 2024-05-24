"""Urls"""

from django.urls import path
from . import views

urlpatterns = [
    path('map/', views.Map.as_view(), name='map'),
    path('', views.start, name='start'),
    path('memories/', views.memories, name='memories'),
    path('auth/', views.auth, name='auth'),
    path('editMemory/<int:mark_id>', views.edit_memory, name='editMemory'),
]
