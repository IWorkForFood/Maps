"""Unit tests for models"""

from django.test import TestCase

# Create your tests here.
from memoryMap.models import MarkedPlaces, Users
class MarkedPlacesModelTest(TestCase):
    """
    Unit test for MarkedPlaces model
    """
    @classmethod
    def setUpTestData(cls):
        """
        Set up MarkedPlaces object for test
        """
        MarkedPlaces.objects.create(
            places_name='TestName',
            about_place='TestDescription',
            x_location=45.325,
            y_location=23.343
        )

    def test_place_label(self):
        """
        Сheck verbose_name field
        """
        test_map = MarkedPlaces.objects.get(id=1)
        field_label = test_map._meta.get_field('about_place').verbose_name
        self.assertEquals(field_label, 'О месте')

    def test_name_label(self):
        """
        Сheck verbose_name field
        """
        test_map = MarkedPlaces.objects.get(id=1)
        field_label = test_map._meta.get_field('places_name').verbose_name
        self.assertEquals(field_label, 'Название места')

    def test_name_max_length(self):
        """
        Сheck if places_name value less than 40 or equal to it
        """
        test_map = MarkedPlaces.objects.get(id=1)
        max_length = test_map._meta.get_field('places_name').max_length
        self.assertTrue(max_length <= 40)


class UsersModelTest(TestCase):
    """
    Unit test for Users model
    """
    @classmethod
    def setUpTestData(cls):
        """
        Create user for test
        """
        Users.objects.create(vk_id='1234')

    def test_first_name_label(self):
        """
        Сheck verbose_name field
        """
        test_user = Users.objects.get(id=1)
        id_label = test_user._meta.get_field('vk_id').verbose_name
        self.assertEquals(id_label, 'id пользователя ВК')

