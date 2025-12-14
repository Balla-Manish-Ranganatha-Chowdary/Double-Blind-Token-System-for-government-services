from rest_framework import generics, permissions
from .models import Citizen
from .serializers import CitizenSerializer

class CitizenCreateView(generics.CreateAPIView):
    queryset = Citizen.objects.all()
    serializer_class = CitizenSerializer
    permission_classes = [permissions.AllowAny]
