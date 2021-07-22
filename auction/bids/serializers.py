from datetime import datetime

from django.utils import timezone

from rest_framework import serializers

from bids.models import Category, Item, Auction, Watchlist, Bid, Autobid
from users.models import UserDetails
from users.serializers import UserDetailsSerializer

def generate_autobid(bid):
    autobid = Autobid.objects.filter(item=bid['auction'].item).all()
    new_bid = bid['price'] + 1
    if autobid:
        for user in autobid.user:
            if user.max_bid - new_bid >= 0 and bid.user != user:
                auction = bid['auction']
                autobid = Bid.objects.create(user=user,auction=auction,price=new_bid)
                user.max_bid -= new_bid
                user.save()

                auction.price=autobid.price
                auction.number_of_bids += 1
                auction.save

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('pk', 'name',)

class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, required=False)
    author = UserDetailsSerializer(required=False)
    image = serializers.ImageField(use_url=True, required=False, allow_null=True)

    def validate(self, data):
        if data['quantity'] <= 0:
            raise serializers.ValidationError({"quantity": "must a valid number"})
        return data

    def create(self, validated_data):
        author = None
        categories_data = None
        if validated_data.get('author', None):            
            author_data = validated_data.pop('author')
            user_data = author_data.pop('user')
            
            user_obj, created = User.objects.get_or_create(**user_data)
            author, created = UserDetails.objects.get_or_create(user=user_obj, **author_data)

        if validated_data.get('category', None):
            categories_data = validated_data.pop('category')

        item = Item.objects.create(author=author, **validated_data)

        if categories_data:
            for categorie_data in categories_data:
                category_obj, category = Category.objects.get_or_create(**categorie_data)
                item.category.add(category_obj)
        return item

    def update(self, instance, validated_data):
        author = None
        if validated_data.get('author', None):
            author_data = validated_data.pop('author')
            user_data = author_data.pop('user')
            
            user_obj, created = User.objects.get_or_create(**user_data)
            author, created = UserDetails.objects.get_or_create(user=user_obj, **author_data)

        instance.name = validated_data['name']
        instance.description = validated_data['description']
        instance.category = validated_data['category']
        instance.author = validated_data['author']
        instance.image = validated_data['image']
        instance.quantity = validated_data['quantity']
        instance.date_posted = validated_data['date_posted']
        instance.active = validated_data['active']

        category_list = []

        if validated_data.get('category', None):
            categories_data = validated_data.pop('category')
            for categorie_data in categories_data:
                category_obj, category = Category.objects.get_or_create(**categorie_data)
                category_list.append(category_obj)
        instance.category = category_list
        instance.save()
        return instance

    class Meta:
        model = Item
        fields = ('pk', 'name', 'description', 'category', 'author', 'image', 'quantity', 'date_posted', 'active',)

class AuctionSerializer(serializers.ModelSerializer):
    def validate(self, data):
        item = data['item']
        if data['time_starting'] > data['time_ending']:
            raise serializers.ValidationError({"time_ending": "must be greater than time_starting"})
        if data['time_starting'] < datetime.now(timezone.utc):
            raise serializers.ValidationError({"time_starting": "must be greater than now time"})
        if data['price'] <= 0:
            raise serializers.ValidationError({"price": "must a valid number"})
        if item.quantity < 0:
            raise serializers.ValidationError({"item": "the item is unavailable"})
        data['number_of_bids'] = 0
        item.quantity -= 1
        item.save()
        return data

    class Meta:
        model = Auction
        fields = ('pk', 'item', 'number_of_bids', 'price', 'time_starting', 'time_ending',)

class WatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = ('pk', 'user', 'auction',)

class AutobidSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Autobid
        fields = ('pk', 'item', 'user',)

class BidSerializer(serializers.ModelSerializer):
    def validate(self, data):
        auction = data['auction']
        if data['bid_time'] < auction.time_starting or data['bid_time'] > auction.time_ending:
            raise serializers.ValidationError({"bid_time": "out of time"})
        if data['price'] < auction.price:
            raise serializers.ValidationError({"price": "must be greater than auction current price"})
        auction.price = data['price']
        auction.number_of_bids += 1
        auction.save()
        generate_autobid(data)
        return data

    class Meta:
        model = Bid
        fields = ('pk', 'user', 'auction', 'price', 'bid_time',)
