from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status, viewsets
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .models import List
from .Serializer import ListSerializer, SignupSerializer, LoginSerializer


class ListViewset(viewsets.ModelViewSet):
    serializer_class = ListSerializer
    permission_classes = [IsAuthenticated]

    # only show tasks of logged-in user
    def get_queryset(self):
        return List.objects.filter(user=self.request.user)

    # automatically set user while creating
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = authenticate(request, username=username, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                response = {
                    "status": status.HTTP_200_OK,
                    "message": "Login successful",
                    "username": user.username,
                    "name": user.first_name,
                    "tokens": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                }
                return Response(response, status=status.HTTP_200_OK)

            return Response(
                {
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "message": "Invalid username or password",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(
            {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Bad request",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class SignupApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "user_id": user.id,
                    "username": user.username,
                    "name": user.first_name,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "status": status.HTTP_400_BAD_REQUEST,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
