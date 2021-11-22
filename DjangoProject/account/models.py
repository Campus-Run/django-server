from django.db import models


class user(models.Model):
    user_seq = models.AutoField(primary_key=True)
    kakao_email = models.EmailField(
        null=True, max_length=254, verbose_name="kakao_email", blank=False)
    kakao_name = models.TextField(null=False, verbose_name="kakao_name")
    kakao_id = models.TextField(null=False, verbose_name="kakao_id")
    hashed_id = models.TextField(
        null=False, verbose_name="hased_kakao_id", default='000')
    univ_name = models.TextField(null=True, verbose_name="univ_name")
    univ_verified = models.BooleanField(default=False)
    first_visit = models.BooleanField(default=True)
    register_dttm = models.DateField(
        auto_now_add=True, verbose_name="register_date")

    def __str__(self):
        return self.kakao_email


class univ(models.Model):
    name = models.CharField(max_length=18, null=False, primary_key=True)
    is_deleted = models.BooleanField(null=False, default=False)
