from django.contrib.auth.models import User
from django.test import TestCase

import json
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from .models import Car, Comment


class CarAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
        data = {'username': 'testuser2', 'password': 'password', 'email': 'testuser@example.com'}
        response = self.client.post('/accounts/api/register/', data, format='json')
        if response.status_code == 200:
            self.token = response.data['token']
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        else:
            print(f"Ошибка регистрации: {response.status_code}")
        # self.token = response.data['token']
        # self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.car = Car.objects.create(make='Toyota', model='Corolla', year=2015, owner=self.user,
                                      description='Описание автомобиля')

    def test_get_cars(self):
        response = self.client.get('/api/cars/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_car(self):
        response = self.client.get('/api/cars/' + str(self.car.pk) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['make'], 'Toyota')

    def test_create_car(self):
        data = {'make': 'Honda', 'model': 'Civic', 'year': 2010, 'owner': self.user.id,
                'description': 'Описание автомобиля'}
        response = self.client.post('/api/cars/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Car.objects.count(), 2)

    def test_update_car(self):
        data = {'make': 'Toyota', 'model': 'Camry', 'year': 2015, 'owner': self.user.id,
                'description': 'Описание автомобиля'}
        response = self.client.put('/api/cars/' + str(self.car.pk) + '/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Car.objects.get(pk=self.car.pk).model, 'Camry')

    def test_delete_car(self):
        response = self.client.delete('/api/cars/' + str(self.car.pk) + '/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Car.objects.count(), 0)

    def test_get_comments(self):
        response = self.client.get('/api/cars/'+str(self.car.pk)+'/comments/')
        self.assertEqual(response.status_code, 200)

    def test_create_comment(self):
        data = {'content': 'Test comment', 'author': self.user.id, 'car': self.car.pk}
        response = self.client.post('/api/cars/' + str(self.car.pk) + '/comments/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), 1)
