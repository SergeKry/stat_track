# Generated by Django 4.2.14 on 2024-08-14 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal_web', '0004_playerprofile_premium_expires'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerprofile',
            name='battles',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='playerprofile',
            name='current_wn8',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
