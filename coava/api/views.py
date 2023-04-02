from django.shortcuts import render
from django.http import HttpResponse, Http404
from rest_framework import views, status, generics, viewsets, mixins
from rest_framework.response import Response
from .serializer import *
from .models import *
from django.db import connection

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

class DailyListView(generics.ListAPIView):
    queryset = Daily.objects.all()
    serializer_class = DailySerializer

class DailyView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView): # 출석체크
    queryset = Daily.objects.all()
    serializer_class = DailySerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, pk, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("UPDATE api_daily SET date = %s where userid_id = %s", [request.data['date'], pk])
        return Response(request.data, status=status.HTTP_200_OK)

class MemeView(viewsets.ModelViewSet): #밈
    queryset = Meme.objects.all()
    serializer_class = MemeSerializer

class BuzzView(viewsets.ModelViewSet): #유행어
    queryset = Buzz.objects.all()
    serializer_class = BuzzSerializer

# class WordView(views.APIView):
    # def get(self, request):