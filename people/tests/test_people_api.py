from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
import json
from people.models import People
from people.serializers import PeopleSerializer
from . import people_sample_data, api_auth_url, api_people_url

class ApiPermissionTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_anonymous_user_cannot_use_people_api(self):
        response = self.client.get(api_people_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put(api_people_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(api_people_url+'1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post(api_people_url+'1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.delete(api_people_url+'1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ApiPeopleTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', '1234')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        for item in people_sample_data:
            People.objects.create(**item)


    def test_api_get_people(self):
        response = self.client.get(api_people_url)

        people = People.objects.all()
        serializer = PeopleSerializer(people, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_api_get_one_people(self):
        response = self.client.get(api_people_url+'1/')

        people = People.objects.get(id="1")
        serializer = PeopleSerializer(people, many=False)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_api_get_one_people_not_found(self):
        response = self.client.get(api_people_url+'9999/')
        response.render()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content), {'detail': 'Not found.'})


    def test_api_post_new_people(self):

        data = {
            "name": "Aditya",
            "surname": "Koss Parisian",
            "code": "9473972",
            "start_date": "2017-07-20",
            "end_date": "2018-01-15",
        }

        response = self.client.post(
            api_people_url,
            data,
            format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        people = People.objects.last()
        serializer = PeopleSerializer(people, many=False)
        self.assertEqual(data['name'], serializer.data['name'])
        self.assertEqual(data['surname'], serializer.data['surname'])
        self.assertEqual(data['code'], serializer.data['code'])
        self.assertEqual(data['start_date'], serializer.data['start_date'])
        self.assertEqual(data['end_date'], serializer.data['end_date'])

    def test_api_post_invalid_new_people(self):

        data = {
            "name": "Aditya",
            "surname": "Koss Parisian",
            "code": "",
            "start_date": "2017-07-20"
        }

        response = self.client.post(
            api_people_url,
            data,
            format="json")

        response.render()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {'code': ['This field may not be blank.']})


    def test_api_post_invalid_end_date(self):

        data = {
            "name": "Chaim",
            "surname": "Dickinson Romaguera",
            "code": "9490287",
            "start_date": "2017-12-21",
            "end_date": "2016-07-20"
        }

        response = self.client.post(
            api_people_url,
            data,
            format="json")

        response.render()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {'code': ['Start date cannot precede end date']})


    def test_api_post_new_people_unique_code(self):

        data = {
            "name": "Nya",
            "surname": "Frami Howell",
            "code": "6771749",
            "start_date": "2015-02-20"
        }

        response = self.client.post(
            api_people_url,
            data,
            format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
            api_people_url,
            data,
            format="json")

        response.render()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {'code':['people with this code already exists.']})


    def test_api_update_people(self):

        data = {
            "name": "Lorena",
            "surname": "Murazik Breitenberg",
            "code": "9071825",
            "start_date": "2017-07-08"
        }

        response = self.client.post(
            api_people_url,
            data,
            format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        people = People.objects.last()

        new_data = {
            "name": "Zachary",
            "surname": "Dietrich Gutmann",
            "code": "7296539",
            "start_date": "2016-12-15"
        }

        response = self.client.put(
            api_people_url+str(people.id)+'/',
            new_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        people = People.objects.last()
        serializer = PeopleSerializer(people, many=False)
        self.assertEqual(new_data['name'], serializer.data['name'])
        self.assertEqual(new_data['surname'], serializer.data['surname'])
        self.assertEqual(new_data['code'], serializer.data['code'])
        self.assertEqual(new_data['start_date'], serializer.data['start_date'])


    def test_api_update_people_not_exist(self):

        new_data = {
            "name": "Deondre",
            "surname": "Rutherford Franecki",
            "code": "2576891",
            "start_date": "2015-08-26"
        }

        response = self.client.put(
            api_people_url+'9999/',
            new_data,
            format="json"
        )

        response.render()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content), {'detail': 'Not found.'})


    def test_api_invalid_update_people(self):

        data = {
            "name": "Laisha",
            "surname": "Collins Corwin",
            "code": "2231562",
            "start_date": "2015-05-08"
        }

        response = self.client.post(
            api_people_url,
            data,
            format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        people = People.objects.last()

        new_data = {
            "name": "Beverly",
            "surname": "West Graham",
            "code": "",
            "start_date": "2017-02-18"
        }

        response = self.client.put(
            api_people_url+str(people.id)+'/',
            new_data,
            format="json"
        )

        response.render()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {'code': ['This field may not be blank.']})

        people = People.objects.last()
        serializer = PeopleSerializer(people, many=False)
        self.assertEqual(data['name'], serializer.data['name'])
        self.assertEqual(data['surname'], serializer.data['surname'])
        self.assertEqual(data['code'], serializer.data['code'])
        self.assertEqual(data['start_date'], serializer.data['start_date'])


    def test_api_delete_people(self):

        data = {
            "name": "Ambrose",
            "surname": "Waters Beahan",
            "code": "9458710",
            "start_date": "2016-06-22"
        }

        response = self.client.post(
            api_people_url,
            data,
            format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        people = People.objects.last()

        response = self.client.delete(
            api_people_url+str(people.id)+'/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(People.DoesNotExist):
            people = People.objects.get(id=people.id)


    def test_api_delete_people_not_exist(self):

        response = self.client.delete(
            api_people_url+'9999/'
        )

        response.render()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content), {'detail': 'Not found.'})

