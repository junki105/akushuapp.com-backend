from django.urls import path

from arapp.api.views import  UserLoginView, UserRegistrationView,  AdminLoginView, EmailVerify, ResetPassword,\
    UserList, PostList

urlpatterns = [
    path('signup', UserRegistrationView.as_view()),
    path('login', UserLoginView.as_view()),
    path('emailverify', EmailVerify.as_view()),
    path('resetPassword', ResetPassword.as_view()),
    path('admin/login', AdminLoginView.as_view()),
    path('users', UserList.as_view()),
    path('users/<uuid:id>', UserList.as_view(), name="get_userDetail"),
    path('posts',PostList.as_view()),
]