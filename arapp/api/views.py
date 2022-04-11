
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404, render
from django.core import serializers
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from arapp.api.serializers import UserLoginSerializer, UserRegistrationSerializer, AdminLoginSerializer
from arapp.api.models import User
from vws import VWS, CloudRecoService
import io
import os

class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'type': 'User registered  successfully',
        }
        return Response(response, status=status_code)

class UserLoginView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data= request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'status code' : status.HTTP_200_OK,
            'token' : serializer.data['token'],
            'refresh':serializer.data['refresh'],
            'email':serializer.data['email'],
            'userStatus':serializer.data['status']
        }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)

class AdminLoginView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AdminLoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data= request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'status code' : status.HTTP_200_OK,
            'token' : serializer.data['token'],
            'refresh':serializer.data['refresh'],
            'email':serializer.data['email']
        }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)

class EmailVerify(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        token = request.GET['token']
        user = User.objects.filter(Q(email_verified_hash=token) & Q(email_verified=False)).first()
        if user:
                user.email_verified = True
                user.status = 1
                user.save()
                status_code = status.HTTP_200_OK
                response = {
                    'success':'true',
                    'status code':status_code,
                }
                return Response(response, status=status_code)
        else:
            status_code = status.HTTP_401_UNAUTHORIZED
            response = {
                'success':'false',
                'status code':status_code,
            }
            return Response(response, status=status_code)

class ResetPassword(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        data = request.data
        email=data['email']
        user = User.objects.filter(email=email).first()
        if not user:
            status_code = status.HTTP_401_UNAUTHORIZED
            response = {
                'success':'false',
                'status code':status_code,
            }
            return Response(response, status=status_code)
        else:
            password = get_random_string(length=8)
            user.set_password(password)
            from_email = settings.DEFAULT_FROM_EMAIL
            from_email = None
            to=[user.email]
            subject = "【】パスワードがリセットされました。"
            message = "【】パスワードがリセットされました。"
            html = '\
            この度は、「」にお申し込み頂きまして<br/>\
            誠にありがとうございます。<br/>\
            <br/>\
            パスワードがリセットされました。。<br/>\
            <br/>\
            　ログインID：' + user.email + '<br/>\
            　パスワード：'+ password + '<br/>\
            ※当メールは送信専用メールアドレスから配信されています。<br/>\
            　このままご返信いただいてもお答えできませんのでご了承ください。<br/>\
            <br/>\
            ※当メールに心当たりの無い場合は、誠に恐れ入りますが<br/>\
            　破棄して頂けますよう、よろしくお願い致します。<br/>'
            send_mail(subject, message, from_email, to, html_message=html)
            user.save()
            status_code = status.HTTP_200_OK
            response = {
                'success':'true',
                'status code':status_code,
            }
            return Response(response, status=status_code)

class UserList(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        user = request.user
        if not user.is_superuser:
            status_code = status.HTTP_401_UNAUTHORIZED
            response = {
                'status code' :status.HTTP_401_UNAUTHORIZED
            }
            return Response(response,status=status_code)
        data = request.data
        keywords = data['Keywords']
        pageNumber = int(data['PageNumber'])
        pageSize = int(data['PageSize'])
        offset = pageSize * (pageNumber - 1)
        if keywords!="":
            userList = User.objects.filter((Q(email__contains=keywords) | Q(name1__contains=keywords) | Q(name__contains=keywords)) & Q(is_superuser = False))[offset:offset+pageSize].values('pk','email','name','avatar')
        else:
            userList = User.objects.filter(Q(is_superuser = False))[offset:offset+pageSize].values('pk','email','name''avatar')
        status_code = status.HTTP_200_OK
        response = {
            'status code' : status.HTTP_200_OK,
            'users': userList,
            'totalRecord': userList.count(),
            'pageCount': (userList.count() / pageSize) + 1
        }
        return Response(response, status=status_code)

    def get(self, request, id):
        user = request.user
        if not user.is_superuser:
            status_code = status.HTTP_401_UNAUTHORIZED
            response = {
                'status code' :status.HTTP_401_UNAUTHORIZED
            }
            return Response(response,status=status_code)
        user = get_object_or_404(User, id=id)
        user_serialized = serializers.serialize('json', [user])
        status_code = status.HTTP_200_OK
        response = {
            'success':'true',
            'status code':status_code,
            'user':user_serialized
        }
        return Response(response, status=status_code)

class UploadView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        server_access_key = '6dde616a95e323b10c829905003f885a46d37653'
        server_secret_key = '7dd11e0fc9798048c5b209cb4fa737c588c14c1d'
        client_access_key = '42e5868a049f7664c88968df024799551c292265'
        client_secret_key = 'b1c056eb779ef77e3661540fd3e7029dfdb76c04'
        fs = FileSystemStorage()
        imageFile =  request.FILES.get('image', '')
        videoFile =  request.FILES.get('video', '')
        videoFilename = fs.save(videoFile.name, videoFile)
        imageFilename = fs.save(imageFile.name, imageFile)
        with open(os.path.join(settings.MEDIA_ROOT, imageFilename), 'rb') as my_image_file:
            my_image = io.BytesIO(my_image_file.read())
        status_code = status.HTTP_201_CREATED
        vws_client = VWS(
            server_access_key=server_access_key,
            server_secret_key=server_secret_key,
        )
        target_id = vws_client.add_target(
            name=videoFilename,
            width=1,
            image=my_image,
            active_flag=True,
            application_metadata=videoFilename,
        )
        response = {
            'success': 'True',
            'status code': status_code,
            'type': 'Video uploaded successfully',
            'imageID':target_id
        }
        return Response(response, status=status_code)
