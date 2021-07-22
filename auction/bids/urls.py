from django.urls import path
from bids import views

urlpatterns = [
    path('categories/', views.CategoryListCreateAPIView.as_view(), name='api-category-list'),
    path('categories/<int:pk>/', views.CategoryDetailsAPIView.as_view(), name='api-category-details'),
    path('items/', views.ItemListCreateAPIView.as_view(), name='api-item-list'),
    path('items/<int:pk>/', views.ItemDetailsAPIView.as_view(), name='api-item-details'),
    path('auctions/', views.AuctionListCreateAPIView.as_view(), name='api-auction-list'),
    path('auctions/<int:pk>/', views.AuctionDetailsAPIView.as_view(), name='api-auction-details'),
    path('watchlists/', views.WatchlistListCreateAPIView.as_view(), name='api-watchlist-list'),
    path('watchlists/<int:pk>/', views.WatchlistDetailsAPIView.as_view(), name='api-watchlist-details'),
    path('bids/', views.BidListCreateAPIView.as_view(), name='api-bid-list'),
    path('bids/<int:pk>/', views.BidDetailsAPIView.as_view(), name='api-bid-details'),
]