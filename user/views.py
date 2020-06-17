from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.settings import api_settings
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from core.models import User
from core.permissions import IsEmployee
from core.helpers import generate_password
from .serializers import UserSerializer, AuthTokenSerializer


class LoginView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


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


class ManageUserView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsEmployee]
    authentication_classes = (TokenAuthentication,)


class ManageUserDetailView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsEmployee]
    authentication_classes = (TokenAuthentication,)


@api_view(['POST'])
@permission_classes([IsEmployee])
@authentication_classes((TokenAuthentication,))
def reset_password(request, pk):
    """Resets users password"""
    query = User.objects.filter(id=pk)
    user = get_object_or_404(query)
    password = generate_password()
    user.set_password(password)
    user.save()
    sts = status.HTTP_202_ACCEPTED
    msg = {'message': "Your password has been successfully updated."}
    email_message = 'Your password has been successfully updated.\n\n' \
                    'Your account information is now:\nEmail: ' + user.email + '\nPassword: ' + password
    email_title = 'Your account password has been reset.'
    send_mail(
        email_title,
        email_message,
        'geomassalas@gmail.com',
        [user.email],
        fail_silently=False,
    )
    return Response(msg, status=sts)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes((TokenAuthentication,))
def reset_password(request, pk):
    """Resets users password"""
    query = User.objects.filter(id=pk)
    user = get_object_or_404(query)
    if request.user == user:
        if 'password' in request.data:
            if 'password2' in request.data:
                if request.data['password'] == request.data['password2']:
                    password = request.data['password']
                    user.set_password(password)
                    user.save()
                    sts = status.HTTP_202_ACCEPTED
                    msg = {'message': "Password successfully updated."}
                    email_message = 'Your password has been successfully updated.\n\n' \
                                    'Your account information is now:\nEmail: ' + user.email + '\nPassword: ' + password
                    email_title = 'Your account password has been reset.'
                    send_mail(
                        email_title,
                        email_message,
                        'geomassalas@gmail.com',
                        [user.email],
                        fail_silently=False,
                    )
                else:
                    msg = {'message': "Passwords do not match."}
                    sts = status.HTTP_400_BAD_REQUEST
            else:
                msg = {'message': "You need to provide a confirmation password."}
                sts = status.HTTP_400_BAD_REQUEST
        else:
            msg = {'message': "You need to provide a new password."}
            sts = status.HTTP_400_BAD_REQUEST
    else:
        msg = {'message': "You are not authorized to change this password."}
        sts = status.HTTP_401_UNAUTHORIZED
    return Response(msg, status=sts)


class DeleteUserView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = (TokenAuthentication,)

