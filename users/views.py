from django.shortcuts import render
from rest_framework import viewsets
from .models import UserProfile
from .serializers import UserProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
