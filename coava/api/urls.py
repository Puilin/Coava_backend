from django.urls import path, include
from rest_framework import routers
from .views import UserListView, JoinView, UserSpecificView, GetUserIDView

urlpatterns = [
    path('user/', UserListView.as_view()),
    path('get_uid/', GetUserIDView.as_view()), #get_uid?nickname=홍길동
    path('mypage/<int:pk>', UserSpecificView.as_view()),
    path('join/', JoinView.as_view()),
]