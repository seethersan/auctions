from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

from users.models import UserDetails

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ManyToManyField(Category, related_name='categories', blank=True)
    author = models.ForeignKey(UserDetails, related_name='posts', on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='images/')
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    date_posted = models.DateTimeField(auto_now_add=True, blank=True)
    active = models.BooleanField()

class Auction(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    number_of_bids = models.IntegerField()
    price = models.FloatField(validators=[MinValueValidator(1.0)])
    time_starting = models.DateTimeField()
    time_ending = models.DateTimeField()

class Watchlist(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

class Autobid(models.Model):    
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    user = models.ManyToManyField(UserDetails, related_name='users', blank=False)

class Bid(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    price = models.FloatField()
    bid_time = models.DateTimeField(default=timezone.now)