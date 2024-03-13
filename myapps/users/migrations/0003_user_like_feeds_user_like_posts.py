# Generated by Django 5.0.3 on 2024-03-11 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0001_initial'),
        ('posts', '0002_post_tag'),
        ('users', '0002_alter_user_created_at_alter_user_login_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='like_feeds',
            field=models.ManyToManyField(related_name='like_feed_users', to='feeds.feed', verbose_name='좋아요한 피드'),
        ),
        migrations.AddField(
            model_name='user',
            name='like_posts',
            field=models.ManyToManyField(related_name='like_post_users', to='posts.post', verbose_name='좋아요한 포스트'),
        ),
    ]
