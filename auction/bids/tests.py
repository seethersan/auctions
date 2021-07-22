from datetime import datetime, timedelta

from rest_framework.test import APITestCase
from rest_framework.views import status

from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from users.models import UserDetails
from bids.models import Category, Item, Auction, Watchlist, Bid

class ItemListCreateAPIView(APITestCase):
    def setUp(self) -> None:
        self.username = 'usuario'
        self.password = 'contrasegna'
        self.data = {
            'username': self.username,
            'password': self.password
        }

        self.url = reverse('api-item-list', kwargs={'version': 'v1'})

    def test_create_item(self):
        url = reverse('jwt-auth')

        user = User.objects.create_user(username='usuario', email='usuario@mail.com', password='contrasegna')

        response = self.client.post(url, self.data, format='json')
        token = response.data['token']

        self.assertEquals(
            Item.objects.count(),
            0
        )

        data = {
            'name': 'name',
            'description': 'description',
            'quantity': 10,
            'active': 1,
            'image': None
        }

        self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(token))
        response = self.client.post(self.url, data=data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(
            Item.objects.count(),
            1
        )
        item = Item.objects.first()
        self.assertEquals(
            item.name,
            data['name']
        )
        self.assertEquals(
            item.description,
            data['description']
        )

    def test_get_item_list(self):
        url = reverse('jwt-auth')

        user = User.objects.create_user(username='usuario', email='usuario@mail.com', password='contrasegna')

        response = self.client.post(url, self.data, format='json')
        token = response.data['token']

        category = Category(name='category_name')
        category.save()
        item = Item(name='name1', description='description1', quantity=10, active=1)
        item.save()
        item.category.add(category)

        self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(token))
        response = self.client.get(self.url, data={'format': 'json'})
        response_json = response.json()
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            len(response_json),
            1
        )
        data = response_json[0]
        self.assertEquals(
            data['name'],
            item.name
        )
        self.assertEquals(
            data['description'],
            item.description
        )
        self.assertEquals(
            data['category'][0]['name'],
            category.name
        )

class AuctionListCreateAPIView(APITestCase):
    def setUp(self) -> None:
        self.username = 'usuario'
        self.password = 'contrasegna'
        self.data = {
            'username': self.username,
            'password': self.password
        }

        self.url = reverse('api-auction-list', kwargs={'version': 'v1'})

    def test_create_auction(self):
        url = reverse('jwt-auth')

        user = User.objects.create_user(username='usuario', email='usuario@mail.com', password='contrasegna')
        item = Item.objects.create(name='name', description='description',quantity=10,active=1,image=None)

        response = self.client.post(url, self.data, format='json')
        token = response.data['token']

        self.assertEquals(
            Auction.objects.count(),
            0
        )

        data = {
            'item': item.id,
            'number_of_bids': 0,
            'price': 10,
            'time_starting': datetime.now(timezone.utc) + timedelta(days=1),
            'time_ending': datetime.now(timezone.utc) + timedelta(days=3)
        }

        self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(token))
        response = self.client.post(self.url, data=data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(
            Auction.objects.count(),
            1
        )
        auction = Auction.objects.first()
        self.assertEquals(
            data['item'],
            auction.item.id
        )
        self.assertEquals(
            data['number_of_bids'],
            auction.number_of_bids
        )        
        self.assertEquals(
            data['price'],
            auction.price
        )
        self.assertEquals(
            data['time_starting'],
            auction.time_starting
        )
        self.assertEquals(
            data['time_ending'],
            auction.time_ending
        )

    def test_get_auction_list(self):
        url = reverse('jwt-auth')

        user = User.objects.create_user(username='usuario', email='usuario@mail.com', password='contrasegna')
        item = Item.objects.create(name='name', description='description',quantity=10,active=1,image=None)

        response = self.client.post(url, self.data, format='json')
        token = response.data['token']

        auction = Auction(item=item, number_of_bids=0, price=10, 
                time_starting=datetime.now(timezone.utc),
                time_ending=datetime.now(timezone.utc) + timedelta(days=3))
        auction.save()

        self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(token))
        response = self.client.get(self.url, data={'format': 'json'})
        response_json = response.json()
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            len(response_json),
            1
        )
        data = response_json[0]
        self.assertEquals(
            data['item'],
            auction.item.id
        )
        self.assertEquals(
            data['number_of_bids'],
            auction.number_of_bids
        )        
        self.assertEquals(
            data['price'],
            auction.price
        )
        self.assertEquals(
            data['time_starting'],
            auction.time_starting.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        )
        self.assertEquals(
            data['time_ending'],
            auction.time_ending.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        )

class BidListCreateAPIView(APITestCase):
    def setUp(self) -> None:
        self.username = 'usuario'
        self.password = 'contrasegna'
        self.data = {
            'username': self.username,
            'password': self.password
        }

        self.url = reverse('api-bid-list', kwargs={'version': 'v1'})

    def test_create_error_bid(self):
        url = reverse('jwt-auth')

        user = User.objects.create_user(username='usuario', email='usuario@mail.com', password='contrasegna')
        item = Item.objects.create(name='name', description='description',quantity=10,active=1,image=None)
        auction = Auction.objects.create(item=item, number_of_bids=0, \
                        price=10, time_starting=datetime.now(timezone.utc),  \
                        time_ending=datetime.now(timezone.utc) + timedelta(days=3))

        response = self.client.post(url, self.data, format='json')
        token = response.data['token']

        self.assertEquals(
            Bid.objects.count(),
            0
        )

        data = {
            'user': user.id,
            'auction': auction.id,
            'price': auction.price - 2,
            'bid_time': datetime.now(timezone.utc)
        }

        self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(token))
        response = self.client.post(self.url, data=data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            Bid.objects.count(),
            0
        )

    def test_create_bid(self):
        url = reverse('jwt-auth')

        user = User.objects.create_user(username='usuario', email='usuario@mail.com', password='contrasegna')
        user_details = UserDetails.objects.create(user=user,max_bid=10,balance=0)
        item = Item.objects.create(name='name', description='description',quantity=10,active=1,image=None)
        auction = Auction.objects.create(item=item, number_of_bids=0, \
                        price=10, time_starting=datetime.now(timezone.utc),  \
                        time_ending=datetime.now(timezone.utc) + timedelta(days=3))

        response = self.client.post(url, self.data, format='json')
        token = response.data['token']

        self.assertEquals(
            Bid.objects.count(),
            0
        )

        data = {
            'user': user_details.id,
            'auction': auction.id,
            'price': 12,
            'bid_time': datetime.now(timezone.utc)
        }

        self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(token))
        response = self.client.post(self.url, data=data, format='json')

        auction = Auction.objects.get(id=data['auction'])

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(
            Bid.objects.count(),
            1
        )
        bid = Bid.objects.first()
        self.assertEquals(
            data['user'],
            bid.user.id
        )
        self.assertEquals(
            data['auction'],
            bid.auction.id
        )        
        self.assertEquals(
            data['price'],
            bid.price
        )
        self.assertEquals(
            auction.number_of_bids,
            1
        )

    def test_create_second_bid_error(self):
        url = reverse('jwt-auth')

        user = User.objects.create_user(username='usuario', email='usuario@mail.com', password='contrasegna')
        user_details = UserDetails.objects.create(user=user,max_bid=10,balance=0)
        item = Item.objects.create(name='name', description='description',quantity=10,active=1,image=None)
        auction = Auction.objects.create(item=item, number_of_bids=0, \
                        price=10, time_starting=datetime.now(timezone.utc),  \
                        time_ending=datetime.now(timezone.utc) + timedelta(days=3))

        response = self.client.post(url, self.data, format='json')
        token = response.data['token']

        self.assertEquals(
            Bid.objects.count(),
            0
        )

        data = {
            'user': user_details.id,
            'auction': auction.id,
            'price': 12,
            'bid_time': datetime.now(timezone.utc)
        }

        self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(token))
        response = self.client.post(self.url, data=data, format='json')

        data['price'] = 11
        data['bid_time'] = datetime.now(timezone.utc)
        response = self.client.post(self.url, data=data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            Bid.objects.count(),
            1
        )

    def test_create_second_bid(self):
        url = reverse('jwt-auth')

        user = User.objects.create_user(username='usuario', email='usuario@mail.com', password='contrasegna')
        user_details = UserDetails.objects.create(user=user,max_bid=10,balance=0)
        item = Item.objects.create(name='name', description='description',quantity=10,active=1,image=None)
        auction = Auction.objects.create(item=item, number_of_bids=0, \
                        price=10, time_starting=datetime.now(timezone.utc),  \
                        time_ending=datetime.now(timezone.utc) + timedelta(days=3))

        response = self.client.post(url, self.data, format='json')
        token = response.data['token']

        self.assertEquals(
            Bid.objects.count(),
            0
        )

        data = {
            'user': user_details.id,
            'auction': auction.id,
            'price': 12,
            'bid_time': datetime.now(timezone.utc)
        }

        self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(token))
        response = self.client.post(self.url, data=data, format='json')

        data['price'] = 13
        data['bid_time'] = datetime.now(timezone.utc)
        response = self.client.post(self.url, data=data, format='json')

        auction = Auction.objects.get(id=data['auction'])

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(
            Bid.objects.count(),
            2
        )
        bid = Bid.objects.order_by('-bid_time').first()
        self.assertEquals(
            data['user'],
            bid.user.id
        )
        self.assertEquals(
            data['auction'],
            bid.auction.id
        )        
        self.assertEquals(
            data['price'],
            bid.price
        )
        self.assertEquals(
            auction.number_of_bids,
            2
        )  
        

    def test_get_bid_list(self):
        url = reverse('jwt-auth')

        user = User.objects.create_user(username='usuario', email='usuario@mail.com', password='contrasegna')
        user_details = UserDetails.objects.create(user=user,max_bid=10,balance=0)
        item = Item.objects.create(name='name', description='description',quantity=10,active=1,image=None)
        auction = Auction.objects.create(item=item, number_of_bids=0, \
                        price=10, time_starting=datetime.now(timezone.utc),  \
                        time_ending=datetime.now(timezone.utc) + timedelta(days=3))

        response = self.client.post(url, self.data, format='json')
        token = response.data['token']

        bid = Bid(user=user_details, auction=auction, price=12, bid_time=datetime.now(timezone.utc))
        bid.save()

        self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(token))
        response = self.client.get(self.url, data={'format': 'json'})
        response_json = response.json()
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            len(response_json),
            1
        )
        data = response_json[0]
        self.assertEquals(
            data['user'],
            bid.user.id
        )
        self.assertEquals(
            data['auction'],
            bid.auction.id
        )        
        self.assertEquals(
            data['price'],
            bid.price
        )