# Generated by Django 5.0.1 on 2024-02-14 09:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0007_rename_nombre_joueur_typejeux_nombre_joueur_max'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partie',
            name='moteur_de_jeu',
        ),
        migrations.AddField(
            model_name='partie',
            name='TypeJeux',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='battle.typejeux'),
        ),
    ]
