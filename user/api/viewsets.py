from rest_framework import viewsets
from .serializers import userSerializers
from user.models import User


class userviewsets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = userSerializers
