# Generated by Django 4.2.2 on 2023-10-03 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_comment_created_comment_updated_post_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_img',
            field=models.ImageField(blank=True, null=True, upload_to='uploaded_img'),
        ),
    ]
