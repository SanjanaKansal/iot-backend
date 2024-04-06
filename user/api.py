from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from user.serializers import UserRegistrationSerializer


class UserViewSet(ModelViewSet):
    def create(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, user_profile = serializer.create(serializer.validated_data)
        return Response({
            "email": user.email,
            "user_type": user_profile.user_type,
            "organization_id": user_profile.organization_id
        })

