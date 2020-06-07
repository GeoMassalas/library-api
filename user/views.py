from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.settings import api_settings
from rest_framework.generics import RetrieveAPIView
from core.models import User
from .serializers import UserSerializer, AuthTokenSerializer


class LoginView(ObtainAuthToken):
    queryset = User.objects.all()
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    permission_classes = [AllowAny]


class ProfileView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        queryset = User.objects.filter(id=request.user.id)
        user = get_object_or_404(queryset)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

