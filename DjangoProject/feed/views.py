from django.shortcuts import render
from feed.models import Ranking, Room
from account.models import user
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http.response import HttpResponse, HttpResponseBadRequest, JsonResponse
# Create your views here.


def ranking(request):
    user_data = user.objects.get(hashed_id=request.headers['token'])
    if request.method == 'GET':

        return JsonResponse({'userName': user_data.kakao_name, 'univName': user_data.univ_name, 'kakaoEmail': user_data.kakao_email}, status=200)


@csrf_exempt
@api_view(['POST'])
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
