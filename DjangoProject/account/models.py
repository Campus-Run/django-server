from django.db import models

class user(models.Model):
  user_seq = models.AutoField(primary_key=True)
  kakao_id = models.TextField(null=False, verbose_name="kakao_id")
  kakao_email = models.EmailField(max_length=254, verbose_name="kakao_email", blank=False)
  kakao_name = models.TextField(null=False, verbose_name="kakao_name")
  register_dttm = models.DateField(auto_now_add=True, verbose_name="register_date")
  univ_name = models.TextField(null=True, verbose_name="univ_name")
  is_active = models.BooleanField(default=False)
  is_first_visit = models.BooleanField(default=True)

  def __str__(self):
      return self.user_email
