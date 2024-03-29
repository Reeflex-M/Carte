# Generated by Django 5.0.1 on 2024-02-14 09:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0008_remove_partie_moteur_de_jeu_partie_typejeux'),
    ]

    operations = [
        migrations.RenameField(
            model_name='partie',
            old_name='TypeJeux',
            new_name='type_jeu',
        ),
        migrations.AlterField(
            model_name='partie',
            name='statut',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='battle.statutpartie'),
        ),
    ]
