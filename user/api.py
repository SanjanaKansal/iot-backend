from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from user.mail import send_activation_mail
from user.models import UserProfile
from user.serializers import LoginSerializer, UserRegistrationSerializer


class UserRegisterViewSet(ModelViewSet):
    def create(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, user_profile = serializer.create(serializer.validated_data)
        send_activation_mail(user=user, token=user_profile.token)
        return Response(
            {
                "message": "Account created successfully. Please check your email to activate the account."
            }
        )


class UserLoginViewSet(ModelViewSet):
    def create(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
            )
            is_verified = UserProfile.objects.filter(
                user__username=serializer.validated_data["email"], is_verified=True
            )
            if not is_verified:
                return Response(
                    {"message": "Please activate your account by checking the email."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if user is not None:
                login(request, user)
                return Response(
                    {"message": "Login successful"}, status=status.HTTP_200_OK
                )
            return Response(
                {"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutViewSet(ModelViewSet):
    def create(self, request, *args, **kwargs):
        logout(request)
        return Response(
            {"message": "Logged out successfully"}, status=status.HTTP_200_OK
        )


class VerifyEmailViewSet(ViewSet):
    @action(methods=["GET"], detail=False, url_path="(?P<token>[^/.]+)")
    def get(self, request, token=None):
        profile = get_object_or_404(UserProfile, token=token)
        if profile:
            profile.is_verified = True
            profile.save()
            return Response(
                {"message": "Email verified successfully"}, status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
        )
