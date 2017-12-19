from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets

from auth_extension.models import UserProfile
from cards.models import BingoCard, BingoCardSquare
from home.models import Contact

from .serializers import (ContactSerializer, BingoCardSerializer,
                          UserSerializer, BingoCardSquareSerializer,
                          UserProfileSerializer)
from .permissions import IsOwnerOrReadOnly, IsUserOrReadOnly


class UserViewset(viewsets.ModelViewSet):
    """
    Read only viewset class for User objects.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfileViewset(viewsets.ModelViewSet):
    """
    Viewset for User Profiles.
    """

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsUserOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class BingoCardViewset(viewsets.ModelViewSet):
    """
    Viewset for Bingo Cards.
    """

    queryset = BingoCard.objects.all()
    serializer_class = BingoCardSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class BingoCardSquareViewset(viewsets.ModelViewSet):
    """
    Viewset for Bingo Card Squares.
    """

    queryset = BingoCardSquare.objects.all()
    serializer_class = BingoCardSquareSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ContactViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for Contact Objects.
    """

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
