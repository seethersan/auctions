from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import filters

from bids.models import Category, Item, Auction, Watchlist, Bid
from bids.serializers import CategorySerializer, ItemSerializer, AuctionSerializer, WatchlistSerializer, BidSerializer

class CategoryListCreateAPIView(ListCreateAPIView):
    """
    API view to retrieve list of posts or create new
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryDetailsAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete post
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class ItemListCreateAPIView(ListCreateAPIView):
    """
    API view to retrieve list of posts or create new
    """
    search_fields = ['name', 'description']
    filter_backends = (filters.SearchFilter,)
    serializer_class = ItemSerializer
    queryset = Item.objects.all()


class ItemDetailsAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete post
    """
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

class AuctionListCreateAPIView(ListCreateAPIView):
    """
    API view to retrieve list of posts or create new
    """
    serializer_class = AuctionSerializer
    queryset = Auction.objects.all()


class AuctionDetailsAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete post
    """
    serializer_class = AuctionSerializer
    queryset = Auction.objects.all()

class WatchlistListCreateAPIView(ListCreateAPIView):
    """
    API view to retrieve list of posts or create new
    """
    serializer_class = WatchlistSerializer
    queryset = Watchlist.objects.all()


class WatchlistDetailsAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete post
    """
    serializer_class = WatchlistSerializer
    queryset = Watchlist.objects.all()

class BidListCreateAPIView(ListCreateAPIView):
    """
    API view to retrieve list of posts or create new
    """
    serializer_class = BidSerializer
    queryset = Bid.objects.all()


class BidDetailsAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete post
    """
    serializer_class = BidSerializer
    queryset = Bid.objects.all()