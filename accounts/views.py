from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """Ro'yxatdan o'tish. Auth talab qilinmaydi."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
        }, status=status.HTTP_201_CREATED)


class ObtainTokenPairView(TokenObtainPairView):
    """Login – token olish. AllowAny."""
    permission_classes = [AllowAny]


class LogoutView(generics.GenericAPIView):
    """Logout – refresh tokenni blacklist qilish."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh = request.data.get('refresh')
            if refresh:
                token = RefreshToken(refresh)
                token.blacklist()
            return Response({'detail': 'Muvaffaqiyatli chiqildi.'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'detail': 'Noto\'g\'ri token.'}, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(generics.RetrieveAPIView):
    """Joriy foydalanuvchi."""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
