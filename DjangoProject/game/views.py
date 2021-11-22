from django.shortcuts import render
from django.http import JsonResponse
from .models import Room
from account.models import user, univ
import hashlib
import json


def create_room(request):
    if request.method == 'POST':
        try:
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
        except:
            return JsonResponse(status=500, data={'status': 500, 'message': "잘못된 입력 데이터입니다."})
    return JsonResponse(status=500, data={'status': 500, 'message': "Request Method가 잘못되었습니다."})


def get_hashed_url(room_id, creater_name):
    key = str(room_id) + creater_name
    return hashlib.sha256(key.encode()).hexdigest()


def check_room_full(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        if('roomURL' not in body or 'count' not in body):
            return JsonResponse(status=500, data={'status': 500, 'message': "필요한 데이터가 없습니다."})
        print(body['roomURL'])
        room_obj = Room.objects.filter(url=body['roomURL'])
        if len(room_obj) == 0:
            return JsonResponse(status=500, data={'status': 500, 'message': "잘못된 입력 데이터입니다."})
        room_obj = room_obj[0]
        if room_obj.max_join <= body['count']:
            return JsonResponse(status=200, data={'status': 200, 'message': "모든 참가자 참여"})
        return JsonResponse(status=200, data={'status': 200, 'message': "참여 대기중"})

    return JsonResponse(status=500, data={'status': 500, 'message': "Request Method가 잘못되었습니다."})
