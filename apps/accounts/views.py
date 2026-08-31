from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import generics, permissions, status
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common.pagination import StandardResultsPagination
from apps.common.permissions import IsAdminOnly

from .serializers import (
    AdminUserSerializer,
    ChangePasswordSerializer,
    LoginSerializer,
    LogoutSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    RegisterSerializer,
    UserSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            token = RefreshToken(serializer.validated_data['refresh'])
            token.blacklist()
        except TokenError:
            return Response({'detail': 'Invalid or already-expired token.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_205_RESET_CONTENT)


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)


class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        if result:
            frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173')
            reset_link = f"{frontend_url}/reset-password?uid={result['uid']}&token={result['token']}"
            send_mail(
                subject='Reset your GolaniSDA password',
                message=f'Use this link to reset your password: {reset_link}',
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@golanisda.org'),
                recipient_list=[result['user'].email],
                fail_silently=True,
            )
        # Always return 200 — never reveal whether the email exists.
        return Response(
            {'detail': 'If an account with that email exists, a reset link has been sent.'},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)


class AdminUserListView(generics.ListAPIView):
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminOnly]
    pagination_class = StandardResultsPagination
    filterset_fields = ['role', 'is_active']
    search_fields = ['email', 'first_name', 'last_name', 'phone']
    ordering_fields = ['created_at', 'email']


class AdminUserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminOnly]
    http_method_names = ['get', 'patch', 'head', 'options']
