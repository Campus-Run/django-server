from django.shortcuts import render
from feed.models import Ranking, Room
from account.models import user, univ
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http.response import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.forms.models import model_to_dict

from account.univ_list import UNIV_LIST
from operator import itemgetter
# Create your views here.


@csrf_exempt
@api_view(['POST'])
def create_ranking(request):
    if request.method == 'POST':
        try:
            user_data = user.objects.get(kakao_email=request.data['name'])
            
            # 기록 이미 존재하는지 확인
            record = Ranking.objects.filter(player=user_data).filter(game_map=request.data['game_map'])
            print(record)
            if len(record) == 0: # 없으면 새로 추가
                ranking = Ranking.objects.create(
                    player=user_data,
                    lap_time=request.data['time'],
                    score=request.data['score'],
                    game_map=request.data['game_map']
                )
                return JsonResponse(status=200, data={'status': 200, 'message': "성공적으로 Ranking을 생성하였습니다.", 'player': user_data.kakao_name})
            else: # 있으면 lap_time이 더 짧은 경우에 수정
                record = record[0]
                if record.lap_time >= request.data['time']:
                    print("출력!!", record.lap_time)
                    record.lap_time=request.data['time']
                    record.score=request.data['score']
                    record.save()
                    return JsonResponse(status=200, data={'status': 200, 'message': "성공적으로 Ranking을 수정하였습니다.", 'player': user_data.kakao_name})
        except:
            return JsonResponse(status=500, data={'status': 500, 'message': "잘못된 입력 데이터입니다."})

@csrf_exempt
@api_view(['GET'])
def speedy_ranking(request, map_id):
    if request.method == 'GET':
        map_list = list(UNIV_LIST.values())
        rankings = Ranking.objects.filter(game_map=map_list[map_id]).order_by('lap_time')
        print(rankings)

        ranking_data = []
        i = 1
        for ranking in rankings:
            user_data=user.objects.get(kakao_email=ranking.player)
            ranking_data.append({
                'rank': i,
                'player': ranking.player.kakao_name,
                'univ': user_data.univ_name,
                'time': ranking.lap_time,
            })
            i+=1

        print(rankings)
        return JsonResponse(status=200, data={'status': 200, 'message': "Speedy Ranking List", 'ranking_data': ranking_data})

@csrf_exempt
@api_view(['GET'])
def univ_ranking(request):
    if request.method == 'GET':
        univ_score = dict(zip(UNIV_LIST.values(), range(len(UNIV_LIST))))
        for key, value in univ_score.items():
            univ_score[key] = 0

        rankings = Ranking.objects.all()
        for ranking in rankings:
            user_data=user.objects.get(kakao_email=ranking.player)
            univ_score[user_data.univ_name] += ranking.score
            print(univ_score[ranking.game_map])

        ranking_data=[]

        for key, value in univ_score.items():
            ranking_data.append({
                'univ': key,
                'score': value,
            })

        ranking_data.sort(key=itemgetter('score'), reverse=True)
        return JsonResponse(status=200, data={'status': 200, 'message': "University Ranking List", 'ranking_data': ranking_data})



@csrf_exempt
@api_view(['POST', 'GET'])
def room(request):
    user_data = user.objects.get(hashed_id=request.headers['token'])
    if request.method == 'POST':
        print(request.data)
        room = Room.objects.create(
            owner=user_data,
            title=request.data['title'],
            owner_university=user_data.univ_name,
            opponent_university=request.data['opponent_university']
        )
        room.hash_key = 'http://localhost:3000/game/' + str(room.id)
        room.save()
        return Response({'owner': room.owner.kakao_name, 'title': room.title, 'ownerUniversity': room.owner_university, 'opponent_university': room.opponent_university, 'room_id': room.id}, status=200)
