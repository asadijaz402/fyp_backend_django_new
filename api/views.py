
from typing import Text
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response
from .serializers import PostCreateSerializer, ResulttCreateSerializer
from rest_framework.decorators import api_view
import json

from rest_framework.permissions import AllowAny

from rest_framework import viewsets
from .FinalBot.BotDetection import getname
from .detection import detecting_fake_news
from .models import Post


import tweepy
import pandas as pd


def gettrends():
    consumer_key = '25SjEQNdimGLs9BNcAfbJW3dA'
    consumer_secret = 'RTt7e2m4iWwbXUUHyH4Vn7YRm6jpoQmm4m8RhedqohQBNbyYLU'
    access_key = '755246834826838016-GPchEozsoRFTm10LbSbUKyG2NlIoLOR'
    access_secret = 'x0LXflU8vJFojsXfgumxLNlh8TEMUCUpqkK5fuH98UY6o'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    import geocoder
    g = geocoder.ip('me')
    get = api.closest_trends(lat=g.latlng[0], long=g.latlng[1])
    cid = get[0].get('parentid')
    trands = api.get_place_trends(id=cid)
    li = []
    for n in trands:
        for a in n.get("trends"):
            if str(a.get("tweet_volume")) != "None":
                a.pop('url')
                a.pop('promoted_content')
                a.pop('query')

                li.append(a)

    trend = json.dumps(li)
    val = eval(trend)

    return val


class get_trends(APIView):
    def get(self, request):
        item = gettrends()
        return Response(item, status=status.HTTP_200_OK)


class Postdata(APIView):

    def post(self, request):
        name = request.data['name']
        text = request.data['text']
        x = getname(name)
        y = detecting_fake_news(text)
        request.data['text_result'] = y
        if x == [1]:
            request.data['name_result'] = False
        else:
            request.data['name_result'] = True

        print(request.data)
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            items = Post.objects.all()
            serializer = PostCreateSerializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        if id:
            item = Post.objects.get(id=id)
            item.delete()
            items = Post.objects.all()
            serializer = PostCreateSerializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        items = Post.objects.all()
        serializer = PostCreateSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
