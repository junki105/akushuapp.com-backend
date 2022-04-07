from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.conf import settings
from arapp.api.models import User
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.utils import timezone

class UserLoginSerializer(TokenObtainPairSerializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    refresh = serializers.CharField(max_length=255, read_only=True)
    status = serializers.IntegerField(read_only=True)
    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        if user.status!=1:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        try:
            data = {}
            refresh = self.get_token(user)
            data['refresh'] = str(refresh)
            data['token'] = str(refresh.access_token)
            data['access_token_expires_in'] = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
            data['refresh_token_expires_in'] = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
            data['email']= user.email
            data['status'] = user.status
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name','email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.email_verified = True
        user.status = 1
        # FRONTEND_URL = settings.FRONTEND_URL
        # token = get_random_string(length=32)
        # verify_link = FRONTEND_URL + '/emailverify/' + token
        # user.email_verified_hash = token
        # now = timezone.now().date()
        # lastdate = now.replace(year=now.year + 100).strftime('%Y-%m-%d')
        # from_email = settings.DEFAULT_FROM_EMAIL
        # from_email = None
        # subject = "【】仮登録完了メール"
        # message = '【】仮登録完了メール'
        # to=[user.email]
        # send_mail(subject, message, from_email, to, html_message=html)
        user.save()
        return user

class AdminLoginSerializer(TokenObtainPairSerializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    refresh = serializers.CharField(max_length=255, read_only=True)
    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        if not user.is_superuser:
            raise serializers.ValidationError(
                'A user with this email and password is not admin.'
            )
        try:
            data = {}
            refresh = self.get_token(user)
            data['refresh'] = str(refresh)
            data['token'] = str(refresh.access_token)
            data['access_token_expires_in'] = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
            data['refresh_token_expires_in'] = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
            data['email']= user.email
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return data