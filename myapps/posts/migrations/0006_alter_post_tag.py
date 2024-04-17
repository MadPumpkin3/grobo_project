# Generated by Django 5.0.3 on 2024-04-03 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0003_feedimage'),
        ('posts', '0005_remove_post_context_post_content_previewpost_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tag',
            field=models.ManyToManyField(blank=True, null=True, related_name='tag_posts', to='feeds.hashtag', verbose_name='태그명'),
        ),
    ]
