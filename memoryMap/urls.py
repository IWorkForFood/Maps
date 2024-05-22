from django.urls import path
from . import views

urlpatterns = [
    path('map/', views.Map.as_view(), name='map'),
    path('auth/', views.auth, name='auth'),
    path('memories/', views.memories, name='memories'),
    path('editMemory/<int:mark_id>', views.edit_memory, name='editMemory'),
]