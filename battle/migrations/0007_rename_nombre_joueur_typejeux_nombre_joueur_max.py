# Generated by Django 5.0.1 on 2024-02-14 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0006_typejeux_nombre_joueur'),
    ]

    operations = [
        migrations.RenameField(
            model_name='typejeux',
            old_name='nombre_joueur',
            new_name='nombre_joueur_max',
        ),
    ]
