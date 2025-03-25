from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from .models import OTPVerification
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role'],
        )
        user.set_password(validated_data['password'])
        user.save()

        # Generate OTP for email verification
        otp = get_random_string(6, allowed_chars='0123456789')
        OTPVerification.objects.create(user=user, otp=otp, expiry_time=timezone.now() + timedelta(minutes=3))
        
        # Send OTP via email
        subject = 'Your OTP for Email Verification'
        message = f'Hello {user.username},\n\nYour OTP for email verification is: {otp}\n\nThis OTP is valid for 3 minutes.'
        recipient_list = [user.email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

        print(f"OTP for {user.username}: {otp}")
        return user

class OTPVerifySerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    otp = serializers.CharField(max_length=6)

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

class ForgotPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)

class ResetPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    new_password = serializers.CharField(write_only=True)
    otp = serializers.CharField(max_length=6)