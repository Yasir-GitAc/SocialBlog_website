# Generated by Django 4.2.2 on 2023-09-05 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_profile_friend_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='type',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
