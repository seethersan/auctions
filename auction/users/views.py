from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from users.models import UserDetails
from users.serializers import UserDetailsSerializer

class UserListCreateAPIView(ListCreateAPIView):
    """
    API view to retrieve list of posts or create new
    """
    serializer_class = UserDetailsSerializer    
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return UserDetails.objects.all()
        else:
            return self.request.user

class UserDetailsAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete post
    """
    serializer_class = UserDetailsSerializer
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return UserDetails.objects.all()
        else:
            return self.request.user