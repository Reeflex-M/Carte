# Generated by Django 5.0.1 on 2024-01-24 09:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0005_partiejoueur_is_bot'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='joueur',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='battle.joueur'),
            preserve_default=False,
        ),
    ]
