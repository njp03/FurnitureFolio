# Generated by Django 3.2.5 on 2021-08-06 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20210806_1513'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='otp',
        ),
    ]
