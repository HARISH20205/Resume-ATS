from django.shortcuts import render
from rest_framework import generics
from .models import EndPoint
from .serializers import EndPointSerializer
# Create your views here.


class EndPointListCreate(generics.ListCreateAPIView):
    queryset = EndPoint.objects.all()
    serializer_class = EndPointSerializer


class EndPointRetriveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = EndPoint.objects.all()
    serializer_class = EndPointSerializer
    lookup_field = 'pk'
