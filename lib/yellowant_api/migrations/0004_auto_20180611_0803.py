# Generated by Django 2.0.6 on 2018-06-11 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yellowant_api', '0003_agile_credentials'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userintegration',
            name='user',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='yellowantredirectstate',
            name='user',
            field=models.IntegerField(),
        ),
    ]
