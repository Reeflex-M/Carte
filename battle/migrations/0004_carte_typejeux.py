# Generated by Django 5.0.1 on 2024-02-01 09:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0003_remove_carte_typejeux'),
    ]

    operations = [
        migrations.AddField(
            model_name='carte',
            name='TypeJeux',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='battle.typejeux'),
        ),
    ]
