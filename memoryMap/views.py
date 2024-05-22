import urllib
from django.core.serializers import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
import requests
from django.views import View
from memoryMap.forms import MarkerForm
from memoryMap.models import MarkedPlaces
import json

# Create your views here.
class Map(View):

    def get(self, request):
        marker_form = MarkerForm()
        return render(request, 'map.html', context={'marker_form': marker_form})

    def post(self, request):
        marker_form = MarkerForm(request.POST)
        if marker_form.is_valid():
            # Получаем текущего пользователя из объекта request
            current_user = request.user

            # Создаем новый экземпляр MarkedPlaces с данными из формы и пользователем
            new_marked_place = MarkedPlaces.objects.create(
                places_name=marker_form.cleaned_data['places_name'],
                about_place=marker_form.cleaned_data['about_place'],
                x_location=marker_form.cleaned_data['x_location'],
                y_location=marker_form.cleaned_data['y_location'],
                user=current_user
            )

            return redirect('/memories/')
        return render(request, 'map.html', context={'marker_form': marker_form})

def auth(request):
    return render(request, 'RegLog.html', {})

def memories(request):
    places_cards = MarkedPlaces.objects.filter(user__username=request.user.username).all();
    return render(request, 'memories.html', {'places_cards':places_cards})

def edit_memory(request, mark_id):
    marked_place = get_object_or_404(MarkedPlaces, pk=mark_id)
    marker_form = MarkerForm()
    if request.method == 'GET':
        json_coords = json.dumps([marked_place.x_location, marked_place.y_location])
        return render(request, 'map.html', {'marker_form': marker_form, 'marked_place':marked_place})

    if request.method == 'POST':
        marker_form = MarkerForm(request.POST)
        if marker_form.is_valid():
            marked_place.places_name = marker_form.cleaned_data['places_name']
            marked_place.about_place = marker_form.cleaned_data['about_place']
            marked_place.x_location = marker_form.cleaned_data['x_location']
            marked_place.y_location = marker_form.cleaned_data['y_location']
            marked_place.save()
            return redirect('/memories/')

    return render(request, 'map.html', {'marker_form': marker_form})

def get_user_data(request):
    if request.method == 'POST':
        silent_token = request.POST.get('silentToken')

        if silent_token:
            # Отправка silent token на сервер VKID для получения данных пользователя
            response = requests.post('https://api.vkid.com/getUserData', data={'silentToken': silent_token})

            if response.status_code == 200:
                user_data = response.json()
                # Обработка данных пользователя, сохранение в базу данных или другие действия

                return JsonResponse({'success': True, 'userData': user_data})

        return JsonResponse({'success': False, 'message': 'Invalid silent token'})

    return JsonResponse({'success': False, 'message': 'Method not allowed'})

