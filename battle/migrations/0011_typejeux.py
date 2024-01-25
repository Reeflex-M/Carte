# Generated by Django 5.0.1 on 2024-01-25 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0010_remove_carte_moteur_de_jeu_carte_moteur_de_jeu'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeJeux',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
                ('logo', models.CharField(max_length=200)),
                ('lien_image', models.CharField(max_length=200)),
                ('moteurs_de_jeu', models.ManyToManyField(to='battle.moteurdejeu')),
            ],
        ),
    ]
