from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegisterView, ObtainTokenPairView, LogoutView, CurrentUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='api_register'),
    path('login/', ObtainTokenPairView.as_view(), name='api_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='api_logout'),
    path('me/', CurrentUserView.as_view(), name='api_me'),
]
