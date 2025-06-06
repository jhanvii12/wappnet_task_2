from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.utils.crypto import get_random_string
from datetime import timedelta
from .models import OTPVerification
from .serializers import UserRegistrationSerializer, OTPVerifySerializer, UserLoginSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
from .permissions import IsAdminUser
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()

class RegisterView(APIView):
    @swagger_auto_schema(request_body=UserRegistrationSerializer, responses={201: 'User registered. Check your email for OTP.'})
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered. Check your email for OTP.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OTPVerifyView(APIView):
    @swagger_auto_schema(request_body=OTPVerifySerializer, responses={200: 'User verified and activated', 400: 'Invalid OTP or user not found'})
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            otp = serializer.validated_data['otp']
            try:
                otp_record = OTPVerification.objects.get(user__username=username, otp=otp)
                if timezone.now() > otp_record.expiry_time:
                    return Response({'error': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)
                otp_record.user.is_active = True
                otp_record.user.save()
                otp_record.delete()
                return Response({'message': 'User verified and activated'})
            except OTPVerification.DoesNotExist:
                return Response({'error': 'Invalid OTP or user not found'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    @swagger_auto_schema(request_body=UserLoginSerializer, responses={200: 'Login successful', 403: 'User not active. OTP sent for reactivation.', 400: 'Invalid credentials'})
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user and user.is_active:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            elif user and not user.is_active:
                print(f"User {user.username} is inactive. Resending OTP...")
                otp = get_random_string(6, allowed_chars='0123456789')
                OTPVerification.objects.create(user=user, otp=otp, expiry_time=timezone.now() + timedelta(minutes=3))
                subject = 'Your OTP for Account Reactivation'
                message = f'Hello {user.username},\n\nYour OTP for account reactivation is: {otp}\n\nThis OTP is valid for 3 minutes.'
                recipient_list = [user.email]
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
                print(f"OTP for re-activation: {otp}")
                return Response({'error': 'User not active. OTP sent for reactivation.'}, status=status.HTTP_403_FORBIDDEN)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    @swagger_auto_schema(request_body=ForgotPasswordSerializer, responses={200: 'OTP sent to email', 404: 'User not found'})
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            try:
                user = User.objects.get(username=username)
                otp = get_random_string(6, allowed_chars='0123456789')
                OTPVerification.objects.create(user=user, otp=otp, expiry_time=timezone.now() + timedelta(minutes=3))
                subject = 'Your OTP for Password Reset'
                message = f'Hello {user.username},\n\nYour OTP for password reset is: {otp}\n\nThis OTP is valid for 3 minutes.'
                recipient_list = [user.email]
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
                print(f"OTP for password reset: {otp}")
                return Response({'message': 'OTP sent to email'})
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    @swagger_auto_schema(request_body=ResetPasswordSerializer, responses={200: 'Password reset successfully', 400: 'Invalid OTP or user not found'})
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            new_password = serializer.validated_data['new_password']
            otp = serializer.validated_data['otp']
            try:
               otp_record = OTPVerification.objects.get(user__username=username, otp=otp)
               if timezone.now() > otp_record.expiry_time:
                    return Response({'error': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)
               user = otp_record.user
               user.set_password(new_password)
               user.save()
               otp_record.delete()
               return Response({'message': 'Password reset successfully'})
            except OTPVerification.DoesNotExist:
                return Response({'error': 'Invalid OTP or user not found'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserEditView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        request_body=UserRegistrationSerializer,
        responses={200: 'User updated', 400: 'Invalid data', 403: 'Permission denied'}
    )
    def put(self, request, username):
        try:
            user = User.objects.get(username=username)
            serializer = UserRegistrationSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'User updated'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class UserDeleteView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(responses={200: 'User deleted', 403: 'Permission denied', 404: 'User not found'})
    def delete(self, request, username):
        try:
            user = User.objects.get(username=username)
            user.delete()
            return Response({'message': 'User deleted'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)