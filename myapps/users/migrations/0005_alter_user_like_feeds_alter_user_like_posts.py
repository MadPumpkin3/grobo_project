# Generated by Django 5.0.3 on 2024-03-21 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0003_feedimage'),
        ('posts', '0003_postimage'),
        ('users', '0004_alter_user_like_feeds_alter_user_like_posts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='like_feeds',
            field=models.ManyToManyField(blank=True, related_name='like_feed_users', to='feeds.feed', verbose_name='좋아요한 피드'),
        ),
        migrations.AlterField(
            model_name='user',
            name='like_posts',
            field=models.ManyToManyField(blank=True, related_name='like_post_users', to='posts.post', verbose_name='좋아요한 포스트'),
        ),
    ]
