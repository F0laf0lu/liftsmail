from django.urls import path
from .views import RegisterView, VerifyEmail
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("signup/", RegisterView.as_view(), name="signup"),
    path("verifyemail/", VerifyEmail.as_view(), name="email-verify"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]