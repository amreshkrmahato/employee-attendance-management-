# Generated by Django 4.0.6 on 2022-07-14 06:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Teache',
            new_name='Mattendences',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='periods',
        ),
    ]