# Generated by Django 5.0.3 on 2024-03-26 13:10

import markdownx.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_postimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='context',
            field=markdownx.models.MarkdownxField(default=None),
            preserve_default=False,
        ),
    ]
