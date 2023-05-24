from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
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
import json

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

class MemeView(viewsets.ModelViewSet): #밈
    queryset = Meme.objects.all()
    serializer_class = MemeSerializer

class BuzzView(viewsets.ModelViewSet): #유행어
    queryset = Buzz.objects.all()
    serializer_class = BuzzSerializer

class ThumbnailView(views.APIView): # 유행어, 밈 썸네일 get
    def get(self, request):
        pk = int(request.GET.get('id', None))
        type = request.GET.get('type', None)
        if type == "buzz":
            try:
                buzz = Buzz.objects.get(id=pk)
                image = buzz.image
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif type == "meme":
            try:
                meme = Meme.objects.get(id=pk)
                image = meme.image
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse(image, content_type='image/png')

class WordView(views.APIView): # 끝말잇기
    def post(self, request):
        url = "https://stdict.korean.go.kr/api/search.do"
        try:
            q = request.data.get('word')
            q = q[-1]
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
        ans_dict = {
            'result' : "SUCCESS",
            'choices' : {
                'word' : word[0]
            }
        }
        return JsonResponse(ans_dict, json_dumps_params={'ensure_ascii': False})

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

class ItemView(views.APIView): # 아이템 개별 이미지
    def get(self, request, pk):
        try:
            item = Item.objects.get(id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        image = item.image
        return HttpResponse(image, content_type='image/png')


class AvatarView(generics.RetrieveUpdateAPIView):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer

    def is_owned(self, user, itemid):
        myitem = MyItem.objects.get(userid=user)
        for i in myitem.items:
            if i == itemid:
                return True
        return False

    def put(self, request, pk, *args, **kwargs):
        try:
            user = User.objects.get(id=pk)
            avatar = Avatar.objects.get(userid=user)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if (self.is_owned(user, request.data['hat']) or\
            self.is_owned(user, request.data['glasses']) or\
                self.is_owned(user, request.data['hair'])):
            with connection.cursor() as cursor:
                cursor.execute("UPDATE api_avatar SET hat_id = %s, glasses_id = %s, hair_id = %s where userid_id = %s", [request.data['hat'], request.data['glasses'], request.data['hair'], pk])
            return Response(request.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class MyItemView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView): # put 편집 필요
    queryset = MyItem.objects.all()
    serializer_class = MyItemSerializer

    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def put(self, request, pk, *args, **kwargs):
        update_list = []
        user = User.objects.get(id=pk)
        myitem = MyItem.objects.get(userid=user)
        items = json.loads(request.data['items'])
        for i in items:
            if i in myitem.items:
                continue
            item = Item.objects.get(id=i) # i is id            
            price = item.price
            if user.token < price:
                update = myitem.items + update_list
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE api_myitem SET items = %s where userid_id = %s", [str(update), pk])
                return Response("That user doesn't have enough token to buy it", status=status.HTTP_402_PAYMENT_REQUIRED)
            with connection.cursor() as cursor: # 구매 액션
                cursor.execute("UPDATE api_user SET token = %s where id = %s", [user.token - price, pk])
            update_list.append(i)
        update = myitem.items + update_list
        with connection.cursor() as cursor:
            cursor.execute("UPDATE api_myitem SET items = %s where userid_id = %s", [str(update), pk])
        myitem = MyItem.objects.get(userid=user)
        return Response(self.serializer_class(myitem).data, status=status.HTTP_200_OK)

