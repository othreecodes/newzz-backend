from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import InterestSerializer
from .models import Interest
# Create your views here.



class InterestViewSet(ModelViewSet):
    serializer_class = InterestSerializer
    queryset = Interest.objects.all()