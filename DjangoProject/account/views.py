from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .email_text import message
from .tokens import account_activation_token
from pathlib import Path
from django.http.response import HttpResponse, HttpResponseBadRequest, JsonResponse
import json
import os
import requests
from django.core.exceptions import ImproperlyConfigured
from .models import user, univ
import hashlib
from django.views.generic import View
from .univ_list import UNIV_DOMAIN, UNIV_LIST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_FILE = os.path.join(BASE_DIR, 'secrets.json')


with open(SECRET_FILE) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} env variable.".format(setting)
        raise ImproperlyConfigured(error_msg)


REST_API_KEY = get_secret('KAKAO_REST_KEY')
REDIRECT_URI = "http://localhost:8000/login/kakao/callback"
API_HOST = 'https://kauth.kakao.com/oauth/authorize?client_id=' + \
    REST_API_KEY+'&redirect_uri='+REDIRECT_URI+'&response_type=code'


def login_view(request):
    return render(request, 'login.html')


def main_view(request):
    return render(request, 'main.html')


def verify_univ_view(request):
    return render(request, 'univ_email.html')


def verify_univ(request):
    try:
        address = request.GET['email']
        mail_domain = address.split('@')[1]
        usr = get_user_by_token(request)
        usr.univ_verified = False
        if UNIV_DOMAIN[0] not in mail_domain and UNIV_DOMAIN[1] not in mail_domain:
            return HttpResponse('fail')
        if mail_domain in UNIV_LIST:
            usr.univ_name = UNIV_LIST[mail_domain]
        print('USER', user)
        mailTitle = "캠퍼스런 이메일 인증을 완료해주세요."
        domain = get_current_site(request).domain
        uidb64 = urlsafe_base64_encode(force_bytes(usr.pk))
        token = account_activation_token.make_token(usr)
        mailData = message(domain, uidb64, token)
        email = EmailMessage(mailTitle, mailData, to=[address])
        email.send()
        usr.save()
        return HttpResponse('success')
    except:
        return HttpResponse('fail')


class Activate(View):
    def get(self, request, uidb64, token):
        # try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        usr = user.objects.get(pk=uid)
        print("Activate:", usr)
        if account_activation_token.check_token(usr, token):
            usr.univ_verified = True
            usr.save()
            return redirect('main')
        return redirect('login')
        # except:
        #   return redirect('login')


def get_user_by_token(request):
    token = request.GET['token']
    print()
    user_qs = user.objects.filter(hashed_id=token)
    if len(user_qs) == 1:
        return user_qs[0]
    return False


def KakaoSignInView(request):
    # return HttpResponse('왜안됨요?')
    return redirect(API_HOST)


def KakaoSignInCallback(request):
    CODE = request.GET['code']
    kakao_token_api = 'https://kauth.kakao.com/oauth/token'
    data = {
        'grant_type': 'authorization_code',
        'client_id': REST_API_KEY,
        'redirection_uri': 'http://localhost:8000/account/login/kakao/callback',
        'code': CODE,
    }

    token_response = requests.post(kakao_token_api, data=data)
    access_token = token_response.json().get('access_token')
    user_info_response = requests.get(
        'https://kapi.kakao.com/v2/user/me', headers={"Authorization": f'Bearer {access_token}'})
    user_info_json = user_info_response.json()

    user_data = {
        'id': '',
        'email': '',
        'nickname': ''
    }

    if 'id' in user_info_json:
        kakao_id = user_info_json['id']
        request.session['kakao_id'] = kakao_id
        user_data['id'] = kakao_id

    if 'kakao_account' in user_info_json:
        if 'email' in user_info_json['kakao_account']:
            user_data['email'] = user_info_json['kakao_account']['email']
        if 'nickname' in user_info_json['kakao_account']['profile']:
            user_data['nickname'] = user_info_json['kakao_account']['profile']['nickname']

    kakao_id = user_data['id']
    hashed_id = hashlib.sha256(str(kakao_id).encode()).hexdigest()

    if isNewface(request, kakao_id):
        if 'email' in user_data:
            user.objects.create(
                kakao_id=kakao_id, kakao_email=user_data['email'], kakao_name=user_data['nickname'], hashed_id=hashed_id)
        else:
            user.objects.create(
                kakao_id=kakao_id, kakao_name=user_data['nickname'], hashed_id=hashed_id)

    return render(request, 'save-token.html', {'idToken': hashed_id})
    # @FIXME: 배포 후 도메인 수정할 것
    # nodeURL = 'http://localhost:3000/kakaoLogin'
    # params = {'idToken': hashed_id}
    # res = requests.get(nodeURL, params=params)
    # print("RES", res)
    # if res.status_code == 200:
    #     # return HttpResponse('200')
    #     return redirect('http://localhost:3000/home')
    # return redirect(nodeURL)
    # return redirect('http://localhost:3000/home')
    # return JsonResponse({'message': 'Register Success'}, status=200)


def isNewface(request, id):
    user_qs = user.objects.filter(kakao_id=id)
    if len(user_qs) == 0:
        return True
    return False


def id_token_check(request):
    token = request.GET['token']
    user_qs = user.objects.filter(hashed_id=token)
    if len(user_qs) == 1:
        return HttpResponse('exist')
    return HttpResponse('not-exist')


def post_user(request):
    print(request.headers['token'])
    user_data = user.objects.get(hashed_id=request.headers['token'])

    return JsonResponse({'userName': user_data.kakao_name, 'univName': user_data.univ_name, 'kakaoEmail': user_data.kakao_email, 'kakaoId': user_data.kakao_id}, status=200)


def api_init_univ_table(request):
    if request.method == 'GET':
        try:
            univ.objects.all().delete()
            print('account.univ table clear')
            for domain, name in UNIV_LIST.items():
                univ.objects.create(name=name, domain=domain)
            return JsonResponse(status=200, data={'status': 200, 'message': "Univ table 초기화 완료"})
        except:
            return JsonResponse(status=500, data={'status': 500, 'message': "Database 처리 에러"})
    return JsonResponse(status=500, data={'status': 500, 'message': "Request Method가 잘못되었습니다."})


def create_dummy_user_data(request):
    user.objects.all().delete()
    user.objects.create(kakao_email="myeong@naver.com", kakao_name="김명준",
                        kakao_id=123123123, hashed_id=123123123, univ_name="중앙대", univ_verified=True)
    user.objects.create(kakao_email="yuniiyuns@naver.com", kakao_name="윤선영",
                        kakao_id=1231231234, hashed_id=1231231234, univ_name="중앙대", univ_verified=True)
    user.objects.create(kakao_email="seogroundwater@naver.com", kakao_name="서지수",
                        kakao_id=1231231235, hashed_id=1231231235, univ_name="숭실대", univ_verified=True)
    user.objects.create(kakao_email="unanchoi@naver.com", kakao_name="최윤한",
                        kakao_id=1231231236, hashed_id=1231231236, univ_name="숭실대", univ_verified=True)
    user.objects.create(kakao_email="yonseikim@naver.com", kakao_name="김연세",
                        kakao_id=1231231237, hashed_id=1231231237, univ_name="연세대", univ_verified=True)
    user.objects.create(kakao_email="seungahkim@naver.com", kakao_name="김승아",
                        kakao_id=1231231238, hashed_id=1231231238, univ_name="연세대", univ_verified=True)
    user.objects.create(kakao_email="zzanggyu@naver.com", kakao_name="이찬규",
                        kakao_id=1231231239, hashed_id=1231231239, univ_name="연세대", univ_verified=True)
    user.objects.create(kakao_email="oereo@naver.com", kakao_name="인세훈",
                        kakao_id=1231231240, hashed_id=1231231240, univ_name="중앙대", univ_verified=True)
    user.objects.create(kakao_email="jwjjy@naver.com", kakao_name="정지원",
                        kakao_id=1231231241, hashed_id=1231231241, univ_name="건국대", univ_verified=True)
    user.objects.create(kakao_email="mocaya@naver.com", kakao_name="김태영",
                        kakao_id=1231231242, hashed_id=1231231242, univ_name="건국대", univ_verified=True)
    return JsonResponse(status=500, data={'status': 200, 'message': "User dummy data 생성 완료"})


def user_search(request):
    if request.method == 'GET':
        keyword = request.GET['keyword']
        qs = user.objects.filter(kakao_name__contains=keyword)
        res = {'data': []}
        for i in range(len(qs)):
            kakao_id = qs[i].kakao_id
            name = qs[i].kakao_name
            univ_name = qs[i].univ_name
            email = qs[i].kakao_email
            obj = {
                'kakao_id': kakao_id,
                'name': name,
                'univ_name': univ_name,
                'email': email
            }
            res['data'].append(obj)
        return JsonResponse(status=200, data={'status': 200, 'message': res})
    return JsonResponse(status=500, data={'status': 500, 'message': "Request Method가 잘못되었습니다."})


def user_by_kakaoid(request):
    if request.method == 'GET':
        kakao_id = request.GET['kakaoId']
        qs = user.objects.filter(kakao_id=kakao_id)[0]
        res = {'data': []}
        kakao_id = qs.kakao_id
        name = qs.kakao_name
        univ_name = qs.univ_name
        email = qs.kakao_email
        obj = {
            'kakao_id': kakao_id,
            'name': name,
            'univ_name': univ_name,
            'email': email
        }
        res['data'].append(obj)
        return JsonResponse(status=200, data={'status': 200, 'message': res})
    return JsonResponse(status=500, data={'status': 500, 'message': "Request Method가 잘못되었습니다."})


@csrf_exempt
@api_view(['POST'])
def check_nickname(request):
    if request.method == 'POST':
        try:
            user_data = user.objects.get(kakao_id=request.data['id'])
            exist_user = user.objects.filter(nickname=request.data['nickname'])
            print(user_data, exist_user)
            if len(exist_user) != 0:
                exist_nickname = user.objects.get(kakao_id=exist_user[0]).nickname
                if user_data.nickname != exist_nickname:
                    # 본인의 닉네임이 아니고, 닉네임을 사용하는 유저가 있는 경우
                    log_data = "존재하는 닉네임입니다."
                    return JsonResponse(status=500, data={'status': 500, 'message': log_data})
                else:
                    return JsonResponse(status=200, data={'status': 200, 'message': "성공적으로 닉네임을 설정하셨습니다.", 'nickname': user_data.nickname})
            if len(request.data['nickname']) >= 15 or len(request.data['nickname']) < 2:
                log_data = "닉네임은 2자에서 15자 이내로 설정해주세요."
                return JsonResponse(status=500, data={'status': 500, 'message': log_data})
            user_data.nickname = request.data['nickname']
            user_data.save()
            return JsonResponse(status=200, data={'status': 200, 'message': "성공적으로 닉네임을 설정하셨습니다.", 'nickname': user_data.nickname})

        except:
            log_data = "잘못된 입력 데이터입니다."
            return JsonResponse(status=500, data={'status': 500, 'message': log_data})
