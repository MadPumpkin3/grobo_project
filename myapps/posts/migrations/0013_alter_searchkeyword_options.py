# Generated by Django 5.0.3 on 2024-04-16 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_alter_searchkeyword_keyword_relation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='searchkeyword',
            options={'ordering': ['-count']},
        ),
    ]
