# Generated by Django 5.0.1 on 2024-01-25 10:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0012_rename_lien_image_typejeux_path_splash'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carte',
            name='moteur_de_jeu',
        ),
        migrations.AddField(
            model_name='carte',
            name='TypeJeux',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='battle.typejeux'),
        ),
    ]
