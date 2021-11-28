from django.shortcuts import render
from django.http import JsonResponse
from .models import Room, Invitation, WaitEntrance, GameEntrance, Record
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
            url = 'http://localhost:3000/game?hash=' + \
                get_hashed_url(room_id, creater_name)
            waiting_url = 'http://localhost:3000/wait?hash=' + \
                get_hashed_url(room_id, creater_name)
            Room.objects.create(url=url, waiting_url=waiting_url, title=title, creater=creater_obj,
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


def room_enter(request):
    if request.method == 'GET':
        try:
            kakao_id = request.GET['kakaoId']
            room_url = request.GET['roomUrl']
            user_obj = user.objects.filter(kakao_id=kakao_id)[0]
            room_obj = Room.objects.filter(url=room_url)[0]
            GameEntrance.objects.create(room=room_obj, user=user_obj)
            return JsonResponse(status=200, data={'status': 200, 'message': "게임 초대를 거절하였습니다."})
        except:
            return JsonResponse(status=500, data={'status': 500, 'message': "잘못된 입력 데이터입니다."})
    return_data = {'status': 500, 'message': "Request Method가 잘못되었습니다."}
    print(return_data)
    return JsonResponse(status=500, data=return_data)


def room_status_by_url(request):
    if request.method == 'GET':
        try:
            current_url = request.GET.get('currentURL')
            room_obj = Room.objects.filter(url__contains=current_url)[0]
            max_join = room_obj.max_join
            curr_join = len(GameEntrance.objects.filter(room=room_obj))
            room_status = max_join - curr_join
            return JsonResponse(status=200, data={'status': 200, 'message': "사용자 입장 정보를 불러왔습니다.", 'data': room_status})
        except:
            return JsonResponse(status=500, data={'status': 500, 'message': "잘못된 입력 데이터입니다."})
    return_data = {'status': 500, 'message': "Request Method가 잘못되었습니다."}
    print(return_data)
    return JsonResponse(status=500, data=return_data)


def new_record(request):
    if request.method == 'GET':
        try:
            kakao_id = request.GET.get('kakaoId')
            current_url = request.GET.get('currentURL')
            start = int(request.GET.get('start'))
            user_obj = user.objects.filter(kakao_id=kakao_id)[0]
            room_obj = Room.objects.filter(url__contains=current_url)[0]
            Record.objects.create(room=room_obj, user=user_obj, start=start)
            return JsonResponse(status=200, data={'status': 200, 'message': "초기 레코드를 생성하였습니다."})
        except:
            return JsonResponse(status=500, data={'status': 500, 'message': "잘못된 입력 데이터입니다."})
    return_data = {'status': 500, 'message': "Request Method가 잘못되었습니다."}
    print(return_data)
    return JsonResponse(status=500, data=return_data)


def update_record(request):
    if request.method == 'GET':
        try:
            kakao_id = request.headers['kakaoId']
            current_url = request.headers['currentURL']
            print("hllo")
            end = int(request.headers['endTime'])
            print(kakao_id, current_url, end)
            user_obj = user.objects.filter(kakao_id=kakao_id)[0]
            room_obj = Room.objects.filter(url__contains=current_url)[0]
            rec_obj = Record.objects.filter(room=room_obj, user=user_obj)[0]
            if rec_obj.end == None:
                print("User: ", kakao_id, "'s end time update!")
                rec_obj.end = end
                rec_obj.save()
            return JsonResponse(status=200, data={'status': 200, 'message': "엔드 레코드를 업데이트하였습니다."})
        except:
            return JsonResponse(status=500, data={'status': 500, 'message': "잘못된 입력 데이터입니다."})
    return_data = {'status': 500, 'message': "Request Method가 잘못되었습니다."}
    print(return_data)
    return JsonResponse(status=500, data=return_data)


def create_room_public(request):
    if request.method == 'GET':
        try:
            title = request.GET['roomTitle']
            max_join = request.GET['maxJoin']
            creater_id = request.GET['createrKakaoId']
            room_id = len(Room.objects.all()) + 1
            creater_obj = user.objects.filter(kakao_id=creater_id)[0]
            creater_name = creater_obj.kakao_name
            creater_univ = creater_obj.univ_name
            home_univ_obj = univ.objects.filter(name=creater_univ)[0]
            url = 'http://localhost:3000/game?hash=' + \
                get_hashed_url(room_id, creater_name)
            waiting_url = 'http://localhost:3000/wait?hash=' + \
                get_hashed_url(room_id, creater_name)
            Room.objects.create(is_public=True, url=url, waiting_url=waiting_url, title=title, creater=creater_obj,
                                owner_univ=home_univ_obj, max_join=max_join)
            return JsonResponse(status=200, data={'status': 200, 'message': "성공적으로 Game Room을 생성하였습니다.", 'url': waiting_url})
        except Exception as e:
            return JsonResponse(status=500, data={'status': 500, 'message': e})
    return_data = {'status': 500, 'message': "Request Method가 잘못되었습니다."}
    print(return_data)
    return JsonResponse(status=500, data=return_data)


def public_room_full_update(request):
    room_qs = Room.objects.filter(is_public=True, is_deleted=False)
    for room_obj in room_qs:
        ent_num = len(WaitEntrance.objects.filter(room=room_obj, is_out=False))
        if(ent_num >= room_obj.max_join):
            room_obj.is_full = True
        else:
            room_obj.is_full = False
        room_obj.save()


def public_room_list(request):
    if request.method == 'GET':
        kakao_id = request.GET['kakaoId']
        univ_name = request.GET['univName']
        univ_obj = univ.objects.filter(name=univ_name)[0]
        public_room_full_update(request)
        home_room_qs = Room.objects.filter(
            is_public=True, owner_univ=univ_obj, is_full=False)
        neutral_room_qs = Room.objects.filter(
            is_public=True, opponent_univ=None, is_full=False)
        away_room_qs = Room.objects.filter(
            is_public=True, opponent_univ=univ_obj, is_full=False)
        room_qs = home_room_qs
        room_qs |= neutral_room_qs
        room_qs |= away_room_qs
        res = {'data': []}
        for i in range(len(room_qs)):
            curr_ent = len(WaitEntrance.objects.filter(
                room=room_qs[i], is_out=False))
            if room_qs[i].opponent_univ == None:
                oppo_univ_name = ""
            else:
                oppo_univ_name = room_qs[i].opponent_univ.name
            obj = {
                'waitingURL': room_qs[i].waiting_url,
                'gameURL': room_qs[i].url,
                'title': room_qs[i].title,
                'homeUniv': room_qs[i].owner_univ.name,
                'opponentUniv': oppo_univ_name,
                'currJoin': curr_ent,
                'maxJoin': room_qs[i].max_join,
            }
            res['data'].append(obj)
        return JsonResponse(status=200, data={'status': 200, 'message': res})
    return_data = {'status': 500, 'message': "Request Method가 잘못되었습니다."}
    print(return_data)
    return JsonResponse(status=500, data=return_data)


def enter_wait_room(request):
    if request.method == 'GET':
        kakao_id = request.GET['kakaoId']
        waiting_url = request.GET['waitingURL']
        user_obj = user.objects.filter(kakao_id=kakao_id)[0]
        univ_obj = univ.objects.filter(name=user_obj.univ_name)[0]
        public_room_full_update(request)
        room_obj = Room.objects.filter(waiting_url=waiting_url)[0]

        if(room_obj.is_full == True):
            return JsonResponse(status=201, data={'status': 201, 'message': "입장 가능 인원을 초과하였습니다.\n다른 방에 입장해주세요!"})

        if(room_obj.owner_univ == univ_obj):
            pass
        else:
            if(room_obj.opponent_univ not in [None, univ_obj]):
                return JsonResponse(status=201, data={'status': 201, 'message': "다른 대학 플레이어가 대기중입니다.\n다른 방에 입장해주세요!"})
            room_obj.opponent_univ = univ_obj
            room_obj.save()
        WaitEntrance.objects.create(room=room_obj, user=user_obj)
        public_room_full_update(request)
        return JsonResponse(status=200, data={'status': 200, 'message': "대기실에 입장합니다."})

    return_data = {'status': 500, 'message': "Request Method가 잘못되었습니다."}
    return JsonResponse(status=500, data=return_data)
