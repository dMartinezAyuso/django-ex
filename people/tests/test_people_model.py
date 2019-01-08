from django.test import TestCase
from django.db import IntegrityError
from people.models import People
from . import people_sample_data

class PeopleTestCase(TestCase):
    def setUp(self):

        self.sample_data = people_sample_data

        for item in self.sample_data:
            People.objects.create(**item)

    def test_can_create_people(self):
        count = People.objects.count()
        self.assertEqual(count, len(self.sample_data))

    def test_uniqueness_code_field(self):
        with self.assertRaises(IntegrityError):
            People.objects.create(**self.sample_data[1])

    def test_people_create_no_end_date_is_active(self):
        person = People.objects.get(code="0403402")

        self.assertIsNone(person.end_date)
        self.assertTrue(person.is_active)

    def test_people_create_no_end_date_is_not_active(self):
        person = People.objects.get(code="0184936")

        self.assertIsNone(person.end_date)
        self.assertFalse(person.is_active)

    def test_people_create_with_end_date_is_active(self):
        person = People.objects.get(code="8899096")

        self.assertIsNotNone(person.end_date)
        self.assertTrue(person.is_active)

    def test_people_create_with_end_date_is_not_active(self):
        person = People.objects.get(code="4535461")

        self.assertIsNotNone(person.end_date)
        self.assertFalse(person.is_active)

        person = People.objects.get(code="9638336")

        self.assertIsNotNone(person.end_date)
        self.assertFalse(person.is_active)