# Generated by Django 5.0.1 on 2024-02-14 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatutPartie',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=200)),
            ],
        ),
    ]
