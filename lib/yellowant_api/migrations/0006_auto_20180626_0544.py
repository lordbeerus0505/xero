# Generated by Django 2.0.6 on 2018-06-26 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yellowant_api', '0005_auto_20180625_0607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xero_credentials',
            name='XERO_STATE',
            field=models.CharField(max_length=1024),
        ),
    ]
