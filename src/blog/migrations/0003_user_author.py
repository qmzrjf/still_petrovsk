# Generated by Django 2.2.10 on 2020-04-30 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='author',
            field=models.BooleanField(default=False),
        ),
    ]
