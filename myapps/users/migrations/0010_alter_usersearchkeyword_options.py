# Generated by Django 5.0.3 on 2024-04-16 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_remove_user_search_keyword_usersearchkeyword'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usersearchkeyword',
            options={'ordering': ['-get_at']},
        ),
    ]