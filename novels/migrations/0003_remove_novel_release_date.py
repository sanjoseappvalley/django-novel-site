# Generated by Django 3.2.4 on 2021-06-12 22:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0002_auto_20210608_2137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='novel',
            name='release_date',
        ),
    ]