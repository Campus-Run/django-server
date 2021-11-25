from django.shortcuts import render
from django.http import JsonResponse
from .models import Room, Invitation
from account.models import user, univ
import hashlib
import json


def create_room(request):
    if request.method == 'GET':
        try:
            title = request.GET['title']
            max_join = request.GET['max_join']
            creater_id = request.GET['creater']
            owner_univ = request.GET['owner_univ']
            opponent_univ = request.GET['opponent_univ']
            room_id = len(Room.objects.all()) + 1
            creater_obj = user.objects.filter(kakao_id=creater_id)[0]
            creater_name = creater_obj.kakao_name
            owner_univ = univ.objects.filter(name=owner_univ)[0]
            opponent_univ = univ.objects.filter(name=opponent_univ)[0]
            url = 'http://localhost:3000/game/' + \
                get_hashed_url(room_id, creater_name)
            Room.objects.create(url=url, title=title, creater=creater_obj,
                                owner_univ=owner_univ, opponent_univ=opponent_univ, max_join=max_join)
            return JsonResponse(status=200, data={'status': 200, 'message': "성공적으로 Game Room을 생성하였습니다.", 'url': url})
        except:
            return JsonResponse(status=500, data={'status': 500, 'message': "잘못된 입력 데이터입니다."})
    return_data = {'status': 500, 'message': "Request Method가 잘못되었습니다."}
    print(return_data)
    return JsonResponse(status=500, data=return_data)


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


def send_invite(request):
    if request.method == 'GET':
        try:
            title = request.GET['title']
            max_join = request.GET['max']
            creater_id = request.GET['creater']
            owner_univ = request.GET['owner_univ']
            opponent_univ = request.GET['opponent_univ']
            home_list = request.GET['homeIdList'].split(',')
            away_list = request.GET['awayIdList'].split(',')
            url = request.GET['url']
            creater_obj = user.objects.filter(kakao_id=creater_id)[0]
            creater_name = creater_obj.kakao_name
            owner_univ_obj = univ.objects.filter(name=owner_univ)[0]
            opponent_univ_obj = univ.objects.filter(name=opponent_univ)[0]

            for home_id in home_list:
                receiver = user.objects.filter(kakao_id=home_id)[0]
                Invitation.objects.create(receiver=receiver, url=url, title=title, creater=creater_obj, home_univ=owner_univ_obj,
                                          away_univ=opponent_univ_obj, is_home=True, max_join=max_join)
            for away_id in away_list:
                receiver = user.objects.filter(kakao_id=away_id)[0]
                Invitation.objects.create(receiver=receiver, url=url, title=title, creater=creater_obj, home_univ=owner_univ_obj,
                                          away_univ=opponent_univ_obj, is_home=False, max_join=max_join)

            return JsonResponse(status=200, data={'status': 200, 'message': "성공적으로 초대장을 전송하였습니다."})
        except:
            return JsonResponse(status=500, data={'status': 500, 'message': "잘못된 입력 데이터입니다."})
    return_data = {'status': 500, 'message': "Request Method가 잘못되었습니다."}
    print(return_data)
    return JsonResponse(status=500, data=return_data)


def invitation_by_id(request):
    if request.method == 'GET':
        try:
            kakao_id = request.GET['kakaoId']
            receiver_obj = user.objects.filter(kakao_id=kakao_id)[0]
            inv_qs = Invitation.objects.filter(
                receiver=receiver_obj, is_read=False)
            result = []
            for qs in inv_qs:
                result.append({
                    'invId': qs.inv_id,
                    'title': qs.title,
                    'creater': qs.creater.kakao_name,
                    'url': qs.url,
                    'receiver': qs.receiver.kakao_name,
                    'homeUniv': qs.home_univ.name,
                    'awayUniv': qs.away_univ.name,
                    'isHome': qs.is_home,
                    'maxJoin': qs.max_join,
                    'isRead': qs.is_read,
                    'createDate': qs.created_at,
                })
            return JsonResponse(status=200, data={'status': 200, 'message': "성공적으로 Game Room을 생성하였습니다.", "data": result})
        except:
            return JsonResponse(status=500, data={'status': 500, 'message': "잘못된 입력 데이터입니다."})
    return_data = {'status': 500, 'message': "Request Method가 잘못되었습니다."}
    print(return_data)
    return JsonResponse(status=500, data=return_data)


def invitation_read(request):
    inv_id = request.GET['invId']
    inst = Invitation.objects.get(inv_id=inv_id)
    inst.is_read = True
    inst.save()
    return JsonResponse(status=200, data={'status': 200, 'message': "초대 읽음 처리 완료"})


def invitation_reject(request):
    if request.method == 'GET':
        try:
            inv_id = request.GET['invId']
            invitation_read(request)
            # @TODO: Need more logic
            return JsonResponse(status=200, data={'status': 200, 'message': "게임 초대를 거절하였습니다."})
        except:
            return JsonResponse(status=500, data={'status': 500, 'message': "잘못된 입력 데이터입니다."})
    return_data = {'status': 500, 'message': "Request Method가 잘못되었습니다."}
    print(return_data)
    return JsonResponse(status=500, data=return_data)
