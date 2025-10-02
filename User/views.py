from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from User.userserializers import UserSerializer, RegisterUserSerializer
from User.models import User
from firebase_admin import auth
from rest_framework.permissions import AllowAny, IsAuthenticated
from firebase import FirebaseAuthentication


class UserViewSetPublic(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    authentication_classes = [] 
    http_method_names = ["get"]

class UserViewSetPrivate(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [FirebaseAuthentication]
    http_method_names = ["get"]

class RegisterUserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.none()
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]
    authentication_classes = [] 
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        #validation
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        first_name = serializer.validated_data.get("first_name", "")
        last_name = serializer.validated_data.get("last_name", "")
        phone = serializer.validated_data.get("phone", "")

        #create in firebase
        try:
            fb_user = auth.create_user(
                email=email,
                password=password,
                display_name=f"{first_name} {last_name}".strip() or None,
                phone_number=phone or None,
            )
        except auth.EmailAlreadyExistsError:
            return Response(
                {"detail": "A user with this email already exists in Firebase."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"detail": f"Firebase error: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        #create in local db
        user = User.objects.create(
            firebase_uid=fb_user.uid,
            email=email,
            username=email, #AbstractUser requires username
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            user_type="USER",
            is_active=True,
        )

        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)