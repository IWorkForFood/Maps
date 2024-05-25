"""Views"""
import json
import urllib
from urllib.parse import urlencode
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
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
    request.session.clear()
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
    send a Silent token(temporary_token from the playlis) in response.
    After receiving the authorization result,
    we exchange the received Silent token for an Access token
    For this we send http request to the url
    Then we receive personal data of user using Access token
    :return: JsonResponse due to unplaned cases, render in case of success
    """
    response = request.GET.get('payload')
    payload = json.loads(response)
    user_uuid = payload['uuid']
    temporary_token = payload['token']

    payload = {
        'v': "5.131",
        'token': temporary_token,
        'access_token': '422847434228474342284743bc4130133444228422847432460238e4efb6cadf0d808ea',
        'uuid': user_uuid,
    }
    encoded_params = urllib.parse.urlencode(payload)
    full_url = f"https://api.vk.com/method/auth.exchangeSilentAuthToken?{encoded_params}"

    server_response = requests.get(full_url)
    response_data = server_response.json()

    permanent_access_token = response_data['response']['access_token']
    vk_user_id = response_data['response']['user_id']
    requested_fields = 'photo_200'

    user_payload = {
        'v': "5.199",
        'access_token': permanent_access_token,
        'fields': requested_fields,
    }
    user_response = requests.get("https://api.vk.com/method/users.get",
                                 params=user_payload)
    user_data = user_response.json()
    user_info = user_data['response'][0]

    user_first_name = user_info['first_name']
    user_photo = user_info['photo_200']
    vk_user_identifier = vk_user_id

    if not Users.objects.filter(vk_id=vk_user_identifier).exists():
        user_entry = Users(vk_id=vk_user_identifier)
        user_entry.save()

    request.session['first_name'] = user_first_name
    request.session['photo_200'] = user_photo
    request.session['user_id'] = vk_user_identifier

    return redirect('/memories/')
