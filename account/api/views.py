from django.contrib.auth.models import User
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
    get_object_or_404,
)

from .serializer import UserSerializer, UserCreateSerializer


class ProfileUpdateAPI(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # lookup_field = "pk"  # default pk

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj


class UserListAPI(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateAPI(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
