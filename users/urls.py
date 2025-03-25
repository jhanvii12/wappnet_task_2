from django.urls import path
from .views import (
    RegisterView,
    OTPVerifyView,
    LoginView,
    ForgotPasswordView,
    ResetPasswordView,
    UserEditView,
    UserDeleteView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', OTPVerifyView.as_view(), name='verify-otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('edit-user/<str:username>/', UserEditView.as_view(), name='edit-user'),
    path('delete-user/<str:username>/', UserDeleteView.as_view(), name='delete-user'),
]