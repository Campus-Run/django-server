# Generated by Django 3.2.7 on 2021-10-04 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='hased_id',
            field=models.TextField(default='000', verbose_name='hased_kakao_id'),
        ),
        migrations.AlterField(
            model_name='user',
            name='kakao_email',
            field=models.EmailField(max_length=254, null=True, verbose_name='kakao_email'),
        ),
    ]
