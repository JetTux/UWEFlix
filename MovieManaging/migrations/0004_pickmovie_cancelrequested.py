# Generated by Django 4.0.3 on 2022-05-04 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MovieManaging', '0003_alter_pickmovie_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='pickmovie',
            name='cancelRequested',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]