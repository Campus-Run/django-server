from django.shortcuts import render
from feed.models import Ranking, Room
from account.models import user
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http.response import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.forms.models import model_to_dict
# Create your views here.


@csrf_exempt
@api_view(['POST', 'GET'])
def ranking(request):
    if request.method == 'POST':
        user_data = user.objects.get(kakao_email=request.data['name'])

        ranking = Ranking.objects.create(
            player=user_data,
            lap_time=request.data['time'],

        )
        return Response({'player': user_data.kakao_name, 'time': ranking.lap_time, 'score': ranking.score}, status=200)

    if request.method == 'GET':
        rankings = Ranking.objects.filter(score=0).order_by('lap_time')

        ranking_data = []
        for ranking in rankings:
            ranking_data.append({
                'player': ranking.player.kakao_name,
                'time': ranking.lap_time,
                'score': ranking.score
            })

        print(rankings)
        return Response({'ranking_data': ranking_data}, status=200)


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
