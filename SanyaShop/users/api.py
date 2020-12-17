from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from users.models import User
from rest_framework.views import APIView
from django.conf import settings
import redis

_redis_instance = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0
)



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserView(APIView):
    def get(
        self,
        request,
        _identificator = None,
    ):
        _redis = redis.StrictRedis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0
    )
        user = []
        if _identificator is not None:
            user = get_object_or_404(User, id=_identificator)
        if str(_redis.get("login")) is None:
            return Response("You are not logged in. Log in to perform such actions.", status=401)
        lgn = _redis.get("login").decode('ascii')
        user = User.objects.filter(login = lgn)[0]
        serializer = UserSerializer(user, many=False)
        dt = serializer.data
        dt.pop('password')
        if user is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(dt)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
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
        if str(_redis.get("login")) is None:
            return Response("You are not logged in. Log in to perform such actions.", status=401)
        lgn = _redis.get("login").decode('ascii')
        user = User.objects.filter(login = lgn)[0]
        print("="*50)
        print(user)
        print("="*50)

        body = request.data
        if 'login' in body:
            return Response("Ви не можуту змінити логінне ім'я.", status=400)
        serializer = UserSerializer(
            user,
            data = request.data,
            partial=True
        )
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data)
        
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(
        self,
        request,
        identificator = None,
    ):
        _redis = redis.StrictRedis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0
    )
        if _redis.get("login") is None:
            return Response("You are not logged in. Log in to perform such actions.", status=401)
        lgn = _redis.get("login").decode()
        user = get_object_or_404(User, login=lgn)

        user.delete()
        _redis.delete("cart")
        _redis.delete("login")
        
        return Response(f"Ви видалили свій аккаунт.")
