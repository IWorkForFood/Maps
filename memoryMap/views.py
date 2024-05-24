"""Views"""

import json
from urllib.parse import urlencode
from django.core.serializers import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views import View
import requests
from memoryMap.forms import MarkerForm
from memoryMap.models import MarkedPlaces
from memoryMap.models import Users

class Map(View):
    """
    Controls behavior of the map-form(form for creating a memory)
    """

    def get(self, request):
        """

        :return: page with form
        """

        marker_form = MarkerForm()
        return render(request, 'map.html', context={'marker_form': marker_form})

    def post(self, request):

        """
        Check if the data is valid to redirect or not to do that

        :return: stay the same page
        """

        marker_form = MarkerForm(request.POST)
        if marker_form.is_valid():
            # Get current user vk_id:
            user_vk_id = request.session.get('user_id', None)
            if user_vk_id is None:
                return HttpResponse("Отсутствует vk_id в сессии пользователя.")

            # Get user by vk_id:
            curr_user = get_object_or_404(Users, vk_id=user_vk_id)

            if not curr_user:
                return HttpResponse("Пользователя нет.")

            # Create new instance with data from the form:
            new_marked_place = MarkedPlaces.objects.create(
                places_name=marker_form.cleaned_data['places_name'],
                about_place=marker_form.cleaned_data['about_place'],
                x_location=marker_form.cleaned_data['x_location'],
                y_location=marker_form.cleaned_data['y_location'],
                user=curr_user
            )
            print("New Marked Place has been created: ", new_marked_place)
            new_marked_place.save()

            return redirect('/memories/')
        return render(request, 'map.html', context={'marker_form': marker_form})

def start(request):
    """
    Open welcome page
    """
    return render(request, 'RegLog.html', {})

def memories(request):
    """
    We get the records made by current user

    :return: page with all the user`s records
    """
    user_vk_id = request.session.get('user_id', None)

    if user_vk_id is None:
        return HttpResponse("Отсутствует vk_id в сессии пользователя.")

    curr_user = get_object_or_404(Users, vk_id=user_vk_id)

    if not curr_user:
        return HttpResponse("Ошибка: Пользователь не найден.")

    places_cards = MarkedPlaces.objects.filter(user=curr_user)
    return render(request, 'memories.html', {'places_cards':places_cards})


def edit_memory(request, mark_id):
    """
    Change data about place in the database

    While Get-request: return to the map-form(map.html) saved data about some place
    While Post-request: Check if the data is correct. If so, then change data
                        to new ones

    :param mark_id: mark_id - id of a record of a place
    :return: template with all places of our user in case of success
            the same template when invalid data are inserted
    """

    marked_place = get_object_or_404(MarkedPlaces, pk=mark_id)
    marker_form = MarkerForm()
    if request.method == 'GET':
        marker_form = MarkerForm(initial={
            'places_name': marked_place.places_name,
            'about_place': marked_place.about_place,
            'x_location': marked_place.x_location,
            'y_location': marked_place.y_location,
        })
        return render(request, 'map.html',
                      {'marker_form': marker_form,
                       'marked_place':marked_place})

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

def auth(request):

    """
    Designed for authentication via VK

    When the user logs in, the VK ID SDK will
    send a Silent token(token from the playlis) in response.
    After receiving the authorization result,
    we exchange the received Silent token for an Access token
    For this we send http request to the url
    Then we receive personal data of user using Access token
    :return: JsonResponse due to unplaned cases, render in case of success
    """

    open_counter = request.session['open_counter'] = request.session.get('open_counter', 0)+1

    if open_counter==1:
        service_token = '422847434228474342284743bc4130133444228422847432460238e4efb6cadf0d808ea'
        if request.method == 'GET':
            payload = request.GET.get('payload')

            if payload:
                payload = json.loads(payload)
                url = "https://api.vk.com/method/auth.exchangeSilentAuthToken"

                params = {
                    'v': "5.131",
                    'token': payload["token"],
                    'access_token': service_token,
                    'uuid': payload["uuid"],
                }

                query_string = urlencode(params)
                url = f'{url}?{query_string}'

                response = requests.post(url)
                first_data = response.json()["response"]

                url = "https://api.vk.com/method/users.get"

                params = {
                    'v': "5.199",
                    'access_token': first_data['access_token'],
                    'fields': "photo_200",
                }

                second_data = {}

                query_string = urlencode(params)
                url = f"{url}?{query_string}"
                response = requests.post(url)
                second_data = json.loads(response.content)["response"]
                first_name = request.session['first_name'] = second_data[0]['first_name']
                photo_200 = request.session['photo_200'] = second_data[0]['photo_200']
                vk_id = request.session['user_id'] = second_data[0]['id']

                if not Users.objects.filter(vk_id = vk_id):
                    new_user = Users(vk_id = vk_id)
                    new_user.save()
                request.session['first_name'] = first_name
                request.session['photo_200'] = photo_200
                request.session['user_id'] = vk_id

                return render(request, 'memories.html')

            return JsonResponse({'success': False, 'message': 'Invalid silent token'})

        return JsonResponse({'success': False, 'message': 'Method not allowed'})

    return render(request, 'memories.html')
