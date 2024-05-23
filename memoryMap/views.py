from django.core.serializers import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
import requests
from django.views import View
from memoryMap.forms import MarkerForm
from memoryMap.models import MarkedPlaces
from memoryMap.models import Users
from urllib.parse import urlencode, urlparse
import json

# Create your views here.

class Map(View):

    def get(self, request):
        marker_form = MarkerForm()
        return render(request, 'map.html', context={'marker_form': marker_form})

    def post(self, request):
        marker_form = MarkerForm(request.POST)
        if marker_form.is_valid():
            # Получаем текущего пользователя
            user_vk_id = request.session.get('user_id', None)
            if user_vk_id is None:
                return HttpResponse("Отсутствует vk_id в сессии пользователя.")

            # Получаем пользователя по vk_id
            curr_user = get_object_or_404(Users, vk_id=user_vk_id)

            if not curr_user:
                return HttpResponse("Пользователя нет.")

            # Создаем новый экземпляр MarkedPlaces с данными из формы и пользователем
            new_marked_place = MarkedPlaces.objects.create(
                places_name=marker_form.cleaned_data['places_name'],
                about_place=marker_form.cleaned_data['about_place'],
                x_location=marker_form.cleaned_data['x_location'],
                y_location=marker_form.cleaned_data['y_location'],
                user=curr_user
            )
            new_marked_place.save()

            return redirect('/memories/')
        return render(request, 'map.html', context={'marker_form': marker_form})

def start(request):
    return render(request, 'RegLog.html', {})

def memories(request):
    print(request.session.get('user_id', None))

    user_vk_id = request.session.get('user_id', None)
    if user_vk_id is None:
        return HttpResponse("Отсутствует vk_id в сессии пользователя.")

    # Получаем пользователя по vk_id
    curr_user = get_object_or_404(Users, vk_id=user_vk_id)

    if not curr_user:
        return HttpResponse("Ошибка: Пользователь не найден.")

    places_cards = MarkedPlaces.objects.filter(user=curr_user);
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

def insertUser(request, id, first_name, photo_200):

    if not Users.objects.filter(vk_id = id):
        new_user = Users(vk_id = id)
    request.session['first_name'] = first_name
    request.session['photo_200'] = photo_200

    return render(request, 'memories.html', {'first_name':first_name, 'photo_200':photo_200, 'id':id})

def auth(request):

    open_counter = request.session['open_counter'] = request.session.get('open_counter', 0)+1;

    if open_counter==1:
        service_token = '422847434228474342284743bc4130133444228422847432460238e4efb6cadf0d808ea'
        #return HttpResponse(request.GET.get('payload'))
        if request.method == 'GET':
            payload = request.GET.get('payload')

            if payload:
                # Отправка silent token на сервер VKID для получения данных пользователя
                payload = json.loads(payload)
                url = "https://api.vk.com/method/auth.exchangeSilentAuthToken"

                params = {
                    'v': "5.131",
                    'token': payload["token"],
                    'access_token': service_token,
                    'uuid': payload["uuid"],
                }
                query_string = urlencode(params)
                parsed_url = urlparse(url)
                url = f'{url}?{query_string}'
                #return HttpResponse(url)

                response = requests.post(url)
                first_data = response.json()["response"]
                #if response.status_code == 200:
                    #user_data = json.loads(response)
                    # Обработка данных пользователя, сохранение в базу данных или другие действия

                    #return HttpResponse(response)

                #return JsonResponse(data)
                url = "https://api.vk.com/method/users.get"

                second_data = {}

                params = {
                    'v': "5.199",
                    'access_token': first_data['access_token'],
                    'fields': "photo_200",
                }

                query_string = urlencode(params)
                url = f"{url}?{query_string}"
                response = requests.post(url)
                second_data = json.loads(response.content)["response"]
                #return HttpResponse(f"{second_data[0]['first_name']}{second_data[0]['photo_200']}{second_data[0]['id']}")
                first_name = request.session['first_name'] = second_data[0]['first_name']
                photo_200 = request.session['photo_200'] = second_data[0]['photo_200']
                id = request.session['user_id'] = second_data[0]['id']

                if not Users.objects.filter(vk_id = id):
                    new_user = Users(vk_id = id)
                    new_user.save()
                request.session['first_name'] = first_name
                request.session['photo_200'] = photo_200
                request.session['user_id'] = id

                return render(request, 'memories.html')

            return JsonResponse({'success': False, 'message': 'Invalid silent token'})

        return JsonResponse({'success': False, 'message': 'Method not allowed'})
    else:
        return render(request, 'memories.html')



