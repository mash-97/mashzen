# Generated by Django 3.1.1 on 2020-10-17 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mashgame', '0005_auto_20201017_0106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='authorized',
        ),
    ]