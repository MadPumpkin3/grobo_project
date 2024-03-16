# Generated by Django 5.0.3 on 2024-03-16 14:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postcomment',
            name='post',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='posts.post', verbose_name='포스트'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postcomment',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자'),
            preserve_default=False,
        ),
        # migrations.CreateModel(
        #     name='PostImage',
        #     fields=[
        #         ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('image_url', models.ImageField(blank=True, null=True, upload_to='post/image', verbose_name='포스트 이미지')),
        #         ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post', verbose_name='포스트')),
        #     ],
        # ),
    ]
