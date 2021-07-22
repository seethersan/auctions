from rest_framework.test import APITestCase
from rest_framework.views import status

from django.urls import reverse
from django.contrib.auth.models import User

from users.models import UserDetails

class JWTAuth(APITestCase):
    def setUp(self) -> None:
        self.username = 'usuario'
        self.password = 'contrasegna'
        self.data = {
            'username': self.username,
            'password': self.password
        }

        self.url = reverse('api-item-list', kwargs={'version': 'v1'})

    def test_current_user(self):

        url = reverse('jwt-auth')

        user = User.objects.create_user(username='usuario', email='usuario@mail.com', password='contrasegna')
        self.assertEqual(user.is_active, 1, 'Active User')

        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.token = response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(self.token))
        response = self.client.get(self.url, data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

class UserDetailsListCreateAPIView(APITestCase):
    def setUp(self) -> None:
        self.username = 'usuario'
        self.password = 'contrasegna'
        self.data = {
            'username': self.username,
            'password': self.password
        }

        self.url = reverse('api-user-list', kwargs={'version': 'v1'})

    def test_create_user(self):
        url = reverse('jwt-auth')

        user = User.objects.create_user(username='usuario', email='usuario@mail.com', \
            password='contrasegna', first_name='hola', last_name='mundo')
        user.is_staff = True
        user.save()

        response = self.client.post(url, self.data, format='json')
        token = response.data['token']

        self.assertEquals(
            UserDetails.objects.count(),
            0
        )

        data = {
            "user":  {
                "username": "usuario2",
                "password": "contrasegna",
                "email": "usuario2@mail.com",
                "first_name": "hola2",
                "last_name": "mundo2"
            },
            "cellphone": "9885785",
            "address": "calle",
            "town": "lima",
            "postal_code": "01455",
            "country": "peru",
            "max_bid": 10,
            "balance": 0
        }

        self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(token))
        response = self.client.post(self.url, data=data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(
            UserDetails.objects.count(),
            1
        )
        user = UserDetails.objects.first()
        self.assertEquals(
            user.cellphone,
            data['cellphone']
        )
        self.assertEquals(
            user.address,
            data['address']
        )
        self.assertEquals(
            user.town,
            data['town']
        )
        self.assertEquals(
            user.postal_code,
            data['postal_code']
        )
        self.assertEquals(
            user.country,
            data['country']
        )
        self.assertEquals(
            user.max_bid,
            data['max_bid']
        )
        self.assertEquals(
            user.balance,
            data['balance']
        )