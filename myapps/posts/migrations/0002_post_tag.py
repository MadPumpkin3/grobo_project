# Generated by Django 5.0.3 on 2024-03-11 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0001_initial'),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tag',
            field=models.ManyToManyField(related_name='tag_posts', to='feeds.hashtag', verbose_name='태그명'),
        ),
    ]
