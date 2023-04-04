from django.shortcuts import render
from django.http import HttpResponse, Http404
import django
from rest_framework import views, status, generics, viewsets, mixins
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from .serializer import *
from .models import *
from django.db import connection
import os
import requests
import random

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

class WordView(views.APIView): # 끝말잇기
    def get(self, request):
        url = "https://stdict.korean.go.kr/api/search.do"
        try:
            q = request.GET.get('word', None)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        params = {
            'key' : os.environ.get('KORAPI_KEY'),
            'q' : q,
            'req_type' : 'json',
            'start' : random.randint(1, 10),
            'advanced' : 'y',
            'method' : 'start',
            'pos' : 1,
            'cat' : [i for i in range(1,64)],
            'letter_s' : 2            
        }
        resp = requests.get(url, params=params)
        resp = resp.json()
        try:
            items = resp['channel']['item']
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        words = list(word['word'] for word in items)
        word = random.sample(words, 1)
        return Response(word[0], status=status.HTTP_200_OK)

class ShopView(views.APIView): # 상점
    def get(self, request):
        try:
            section_name = request.GET.get('section', None)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        section = Section.objects.get(section_name=section_name)
        itemset = section.item_set.all()
        json = django.core.serializers.serialize('json', itemset, ensure_ascii=False)
        return HttpResponse(json, content_type='application/json', charset='utf-8')

class ItemView(views.APIView):
    def get(self, request, pk):
        try:
            item = Item.objects.get(id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        image = item.image
        return HttpResponse(image, content_type='image/png')