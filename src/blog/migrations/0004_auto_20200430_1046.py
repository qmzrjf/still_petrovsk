# Generated by Django 2.2.10 on 2020-04-30 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_user_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='author',
            new_name='author_status',
        ),
    ]
