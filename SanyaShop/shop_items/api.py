from shop_items.models import ShoppingItem
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
import redis


class ShoppingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingItem
        fields = '__all__'

class ShoppingItemView(APIView):
    def get(self, request, _identificator = None):
        if 'category' in request.GET.keys():
            cat = request.GET['category']
            if cat == "":
                data = ShoppingItem.objects.all()
                serializer = ShoppingItemSerializer(data, many = True)
                return Response(serializer.data)
            data = ShoppingItem.objects.filter(category=cat)
            serializer = ShoppingItemSerializer(data, many=True)
            return Response(serializer.data)
    
        if _identificator is None:
            data = ShoppingItem.objects.all()
            serializer = ShoppingItemSerializer(data, many = True)
            return Response(serializer.data)
        elif 'category/' not in _identificator:
            try:
                ide = int(_identificator)
                data = get_object_or_404(ShoppingItemView, id=ide)
                serializer = ShoppingItemSerializer(data)
                return Response(serializer.data)
            except ValueError as e:
                pass
            except Exception as e:
                return Response("Such item does not exist.")
        
        
    def post(self, request):
        _redis = redis.StrictRedis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0
    )
        if _redis.get("login") is None:
            return Response("You are not logged in. Log in to perform such actions.", status=401)
        dt = request.data
        dt['creator'] = _redis.get("login").decode()
        serializer = ShoppingItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def patch(
        self,
        request
    ):
        _redis = redis.StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0
        )
        body = request.data
        if _redis.get("login") is None:
            return Response("You are not logged in. Log in to perform such actions.", status=401)
        item_id = body['id']
        item = get_object_or_404(ShoppingItem, id = item_id)
        usr = _redis.get("login").decode()
        if item.creator == usr:
            serializer = ShoppingItemSerializer(
                item,
                data = request.data,
                partial=True
            )
            if serializer.is_valid():
                user = serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=401)

        return Response("You are not authorized to change this message.", status=401)


    def delete(self,request,):
        _redis = redis.StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0
        )
        body = request.data
        if _redis.get("login") is None:
            return Response("You are not logged in. Log in to perform such actions.", status=401)
        item_id = body['id']
        item = get_object_or_404(ShoppingItem, id = item_id)
        usr = _redis.get("login").decode()
        if item.creator == usr:
            item.delete()
            return Response("Item deleted.")
        return Response("You are not authorized to change this message.", status=401)
        




