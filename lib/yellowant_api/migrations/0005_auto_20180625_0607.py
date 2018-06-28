# Generated by Django 2.0.6 on 2018-06-25 06:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yellowant_api', '0004_auto_20180611_0803'),
    ]

    operations = [
        migrations.CreateModel(
            name='Xero_Credentials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('XERO_STATE', models.CharField(max_length=256)),
                ('XERO_UPDATE_LOGIN_FLAG', models.BooleanField(default=False)),
                ('user_integration', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='yellowant_api.UserIntegration')),
            ],
        ),
        migrations.RemoveField(
            model_name='agile_credentials',
            name='user_integration',
        ),
        migrations.DeleteModel(
            name='Agile_Credentials',
        ),
    ]
