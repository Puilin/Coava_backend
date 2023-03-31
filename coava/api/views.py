from django.shortcuts import render
from django.http import HttpResponse, Http404
from rest_framework import views, status, generics, viewsets
from rest_framework.response import Response
from .serializer import UserSerializer, DailySerializer, MemeSerializer, BuzzSerializer
from .models import User, Daily, Meme, Buzz

# Create your views here.
class UserListView(generics.ListAPIView): # user 전체 목록 출력
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserSpecificView(generics.RetrieveUpdateAPIView): # mypage용 view (User ID 필요함)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GetUserIDView(views.APIView): # User ID를 반환하는 view
    def get(self, request):
        try:
            user = User.objects.get(nickname=request.GET.get('nickname', None))
            return Response(user.id, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            raise Http404

class JoinView(generics.CreateAPIView): # 회원가입 용 view
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DailyView(viewsets.ModelViewSet): # 출석체크
    queryset = Daily.objects.all()
    serializer_class = DailySerializer

class MemeView(viewsets.ModelViewSet): #밈
    queryset = Meme.objects.all()
    serializer_class = MemeSerializer

class BuzzView(viewsets.ModelViewSet): #유행어
    queryset = Buzz.objects.all()
    serializer_class = BuzzSerializer