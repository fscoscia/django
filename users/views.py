from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import UserProfile
from .serializers import UserProfileSerializer
from django.contrib.auth.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
