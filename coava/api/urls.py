from django.urls import path, include
from rest_framework import routers
from .views import *

urlpatterns = [
    path('user/', UserListView.as_view()),
    path('get_uid/', GetUserIDView.as_view()), #get_uid?nickname=홍길동
    path('mypage/<int:pk>', UserSpecificView.as_view()), # 마이페이지
    path('mypage/avatar/<int:pk>', AvatarView.as_view()), # 마이페이지 (아바타)
    path('myitem/<int:pk>', MyItemView.as_view()), # 구매
    path('join/', JoinView.as_view()),
    path('daily/', DailyListView.as_view()), # 출석 리스트
    path('daily/<int:pk>/', DailyView.as_view()), #출석
    path('meme/', MemeView.as_view({ #밈
        'get' : 'list',
        'post' : 'create',
        'put' : 'update'
    })),
    path('buzz/', BuzzView.as_view({ #유행어
        'get' : 'list',
        'post' : 'create',
        'put' : 'update'
    })),
    path('thumbnail/', ThumbnailView.as_view()),
    path('word/', WordView.as_view()),
    path('shop/', ShopView.as_view()),
    path('item/<int:pk>', ItemView.as_view())
]