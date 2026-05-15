from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserProfileSerializer
from .models import CustomUser

# register view
class RegisterView(APIView):
    permission_classes=[permissions.AllowAny]
    def post(self, request):
        serializer=RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message":"User registerd succssfully"
                },
                status=status.HTTP_201_CREATED
            )
            
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        
# login page

class LoginView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):

        email = request.data.get("email")
        password = request.data.get("password")

        # authenticate user using email
        user = authenticate(
            request,
            username=email,
            password=password
        )

        # login success
        if user is not None:

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "message": "login successful",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK
            )

        # invalid credentials
        return Response(
            {
                "error": "Invalid email or password"
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
        
class UserProfilView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    
    def get(self, request):
        user= request.user
        
         # Convert user data to JSON
        serializer= UserProfileSerializer(user)
        
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )