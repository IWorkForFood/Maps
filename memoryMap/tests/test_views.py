from django.test import TestCase, RequestFactory

from django.urls import reverse
from memoryMap.models import MarkedPlaces, Users
from memoryMap.forms import MarkerForm
from django.forms.models import model_to_dict

class MemoriesViewTest(TestCase):
    """
    Test view memories(Ruturn list of impressions)
    """

    @classmethod
    def setUpTestData(cls):
        cls.vk_user = Users.objects.create(vk_id="1234")
        number_of_map_cards = 2
        for card_num in range(number_of_map_cards):
            MarkedPlaces.objects.create(places_name='TestName', about_place ='TestDescription', x_location=45.325, y_location= 23.343, user=cls.vk_user)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/memories/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('memories'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        session = self.client.session
        session['user_id'] = self.vk_user.vk_id
        session.save()
        resp = self.client.get(reverse('memories'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'memories.html')

    def test_data_creation(self):
        session = self.client.session
        session['user_id'] = self.vk_user.vk_id
        session.save()
        resp = self.client.get(reverse('memories'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([model_to_dict(x) for x in resp.context['places_cards']], [{'id': 1, 'places_name': 'TestName', 'about_place': 'TestDescription', 'x_location': 45.325, 'y_location': 23.343, 'user': 1}, {'id': 2, 'places_name': 'TestName', 'about_place': 'TestDescription', 'x_location': 45.325, 'y_location': 23.343, 'user': 1}])

class MapViewTest(TestCase):

    """
    Test view Map(Create impression about place)
    """

    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.vk_user = Users.objects.create(vk_id="1234")

        cls.invalid_data = {
            'places_name': '',
            'about_place': '',
            'x_location': 45.325,
            'y_location': 23.343,
        }
        cls.valid_data = {
            'places_name': 'TestName',
            'about_place': 'TestDescription',
            'x_location': 45.325,
            'y_location': 23.343,
        }

    def tearDown(self):
        Users.objects.all().delete()

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('map'))
        self.assertEqual(resp.status_code, 200)

    def test_view_get_request(self):
        session = self.client.session
        session['user_id'] = self.vk_user.vk_id
        session.save()
        resp = self.client.get(reverse('map'))
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.context['marker_form'], MarkerForm)
        self.assertTemplateUsed(resp, 'map.html')

    def test_view_post_request_with_valid_data(self):
        session = self.client.session
        session['user_id'] = self.vk_user.vk_id
        session.save()

        resp = self.client.post(reverse('map'), self.valid_data, follow=True)
        self.assertEqual(MarkedPlaces.objects.count(), 1)

    def test_view_post_request_with_invalid_data(self):
        session = self.client.session
        session['user_id'] = self.vk_user.vk_id
        session.save()
        resp = self.client.post(reverse('map'), self.invalid_data)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'map.html')
        self.assertEqual(MarkedPlaces.objects.count(), 0)

