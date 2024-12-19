from rest_framework import generics
from .models import Furniture
from .serializers import FurnitureSerializer
from django.shortcuts import render
from django.http import HttpResponse

class FurnitureListView(generics.ListAPIView):
    queryset = Furniture.objects.all()
    serializer_class = FurnitureSerializer

class FurnitureDetailView(generics.RetrieveAPIView):
    queryset = Furniture.objects.all()
    serializer_class = FurnitureSerializer
    lookup_field = 'furniture_id'

