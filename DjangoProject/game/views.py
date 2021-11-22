from django.shortcuts import render
from django.http import JsonResponse
from .models import Room
from account.models import user, univ
import hashlib
import json


def create_room(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        if('title' not in body or 'creater' not in body or 'owner_univ' not in body or 'opponent_univ' not in body or 'max_join' not in body):
            return JsonResponse(status=500, data={'status': 500, 'message': "필요한 데이터가 없습니다."})
        room_id = len(Room.objects.all()) + 1
        creater_id = body['creater']
        creater_obj = user.objects.filter(user_seq=creater_id)[0]
        creater_name = creater_obj.kakao_name
        owner_univ = univ.objects.filter(name=body['owner_univ'])[0]
        opponent_univ = univ.objects.filter(name=body['opponent_univ'])[0]
        url = get_hashed_url(room_id, creater_name)
        Room.objects.create(url=url, title=body['title'], creater=creater_obj,
                            owner_univ=owner_univ, opponent_univ=opponent_univ, max_join=body['max_join'])
        return JsonResponse(status=200, data={'status': 200, 'message': "성공적으로 Game Room을 생성하였습니다."})

    return JsonResponse(status=500, data={'status': 500, 'message': "Request Method가 잘못되었습니다."})


def get_hashed_url(room_id, creater_name):
    key = str(room_id) + creater_name
    return hashlib.sha256(key.encode()).hexdigest()
