# Generated by Django 4.0.3 on 2022-04-18 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_clubdetails_clubrep'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentclub',
            name='club',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='accounts.clubdetails'),
        ),
    ]
