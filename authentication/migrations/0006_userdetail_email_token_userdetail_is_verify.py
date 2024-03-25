# Generated by Django 4.2.11 on 2024-03-23 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_rename_country_userdetail_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetail',
            name='email_token',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userdetail',
            name='is_verify',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
