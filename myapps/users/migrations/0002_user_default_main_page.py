# Generated by Django 5.0.3 on 2024-03-19 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='default_main_page',
            field=models.IntegerField(default=0, verbose_name='기본 메인 페이지'),
        ),
    ]
