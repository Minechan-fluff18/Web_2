from django.conf import settings
from json import loads, dumps
from django.http import HttpResponse
import redis
from users.models import User
from shop_items.models import ShoppingItem
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


def like(request):
    _redis = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0
    )
    if _redis.get("login") is None:
        return HttpResponse("You are not logged in. Log in to perform such actions.", status=401)
    body = loads(request.body)
    item = get_object_or_404(ShoppingItem, id=body['id'])
    user = get_object_or_404(User, login=_redis.get("login").decode())
    likes = user.likes
    if likes == None:
        likes = []
    if item.id in likes:
        return HttpResponse("Ви вже лайкнули цей товар.")
    likes.append(item.id)
    user.likes = likes
    user.save()
    item.likes = item.likes + 1
    item.save()
    print(item.likes)
    return HttpResponse(item.likes)
