# Generated by Django 4.2.2 on 2023-09-10 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_rename_timestamp_message_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='seen',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
