# Generated by Django 4.2.10 on 2024-03-23 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_material_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userdetail',
            old_name='Country',
            new_name='country',
        ),
        migrations.RenameField(
            model_name='userdetail',
            old_name='Gender',
            new_name='gender',
        ),
        migrations.RemoveField(
            model_name='userdetail',
            name='firstname',
        ),
        migrations.RemoveField(
            model_name='userdetail',
            name='lastname',
        ),
    ]
