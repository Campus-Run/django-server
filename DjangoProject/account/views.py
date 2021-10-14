from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .email_text import message
from .tokens import account_activation_token
from pathlib import Path
from django.http.response import HttpResponse, HttpResponseBadRequest, JsonResponse
import json, os, requests
from django.core.exceptions import ImproperlyConfigured
from .models import user
import hashlib
from django.views.generic import View
from .univ_list import UNIV_DOMAIN, UNIV_LIST


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
API_HOST = 'https://kauth.kakao.com/oauth/authorize?client_id='+REST_API_KEY+'&redirect_uri='+REDIRECT_URI+'&response_type=code'


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
    print('USER',user)
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
  user_info_response = requests.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization": f'Bearer {access_token}'})
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
      user.objects.create(kakao_id=kakao_id, kakao_email=user_data['email'], kakao_name=user_data['nickname'], hashed_id=hashed_id) 
    else:
      user.objects.create(kakao_id=kakao_id, kakao_name=user_data['nickname'], hashed_id=hashed_id) 
  
  # @FIXME: 배포 후 도메인 수정할 것
  nodeURL = 'http://localhost:3000/kakaoLogin'
  params = {'idToken': hashed_id}
  res = requests.get(nodeURL, params=params)
  print("RES",res)
  if res.status_code == 200:
    return redirect('http://localhost:3000/')
  return redirect(nodeURL)
  

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