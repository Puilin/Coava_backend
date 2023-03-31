from django.urls import path, include
from rest_framework import routers
from .views import UserListView, JoinView, UserSpecificView, GetUserIDView, DailyView, MemeView, BuzzView

urlpatterns = [
    path('user/', UserListView.as_view()),
    path('get_uid/', GetUserIDView.as_view()), #get_uid?nickname=홍길동
    path('mypage/<int:pk>', UserSpecificView.as_view()),
    path('join/', JoinView.as_view()),
    path('daily/<int:pk>', DailyView.as_view({ #출석
        'get' : 'retrieve',
        'put' : 'update',
        'post' : 'create'
    })),
    path('meme/', MemeView.as_view({ #밈
        'get' : 'list',
        'post' : 'create',
        'put' : 'update'
    })),
    path('buzz/', BuzzView.as_view({ #유행어
        'get' : 'list',
        'post' : 'create',
        'put' : 'update'
    }))
]