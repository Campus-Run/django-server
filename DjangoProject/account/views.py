from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .email_text import message
from .tokens import account_activation_token


def login_view(request):
  return render(request, 'login.html')


def main_view(request):
  return render(request, 'main.html')


def verify_univ(request, user):
  address = request.GET['email']
  mailTitle = "캠퍼스런 이메일 인증을 완료해주세요."
  domain = get_current_site(request).domain
  uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
  token = account_activation_token.make_token(user)
  mailData = message(domain, uidb64, token)
  email = EmailMessage(mailTitle, mailData, to=[address])
  email.send()