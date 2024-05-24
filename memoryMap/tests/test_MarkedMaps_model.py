from django.test import TestCase

# Create your tests here.
from memoryMap.models import MarkedPlaces, Users
class MarkedPlacesModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        MarkedPlaces.objects.create(places_name='TestName', about_place ='TesDescription', x_location=45.325, y_location= 23.343)

    def test_place_label(self):
        test_map = MarkedPlaces.objects.all().first()
        field_label = test_map._meta.get_field('about_place').verbose_name
        self.assertEquals(field_label,'О месте')

    def test_name_label(self):
        test_map  = MarkedPlaces.objects.all().first()
        field_label = test_map._meta.get_field('places_name').verbose_name
        self.assertEquals(field_label,'Название места')

    def test_name_max_length(self):
        test_map  = MarkedPlaces.objects.all().first()
        max_length = test_map._meta.get_field('places_name').max_length
        self.assertTrue(max_length <= 40)

    def test_str(self):
        test_map = MarkedPlaces.objects.all().first()
        expected_object_name = test_map.places_name
        self.assertEquals(expected_object_name, str(test_map))

class UsersModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Users.objects.create(vk_id='1234')

    def test_first_name_label(self):
        test_user = Users.objects.all().first()
        id_label = test_user._meta.get_field('vk_id').verbose_name
        self.assertEquals(id_label, 'id зашедшего пользователя в вк')

