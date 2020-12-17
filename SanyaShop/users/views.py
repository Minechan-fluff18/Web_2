from django.conf import settings
from json import loads
from django.http import HttpResponse
from users.models import User
import redis


_redis_instance = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0
)

def login(request, redis_instance = _redis_instance):
    if redis_instance.get('login'):
        return HttpResponse("Ви вже увійшли до системи.")
    data = loads(request.body)

    filtered = User.objects.filter(login=data['login']).filter(password=data['password'])
    if len(filtered) != 1:
        return HttpResponse("Вводні данні не є вірними. Спробуйте ще раз.")
        
    user = filtered[0]
    redis_instance.set('login', data['login'])
    return HttpResponse("Ви успішно увійшли до системи.")


def logout(request, redis_instance = _redis_instance):
    if redis_instance.get('login'):
        redis_instance.delete('login')
        redis_instance.delete('cart')
        return HttpResponse("Ви успішно вийшли з системи.")
    return HttpResponse("Вас нема у системі.")

