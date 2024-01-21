# Generated by Django 5.0 on 2024-01-21 16:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_alter_achat_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Doit',
        ),
        migrations.AddField(
            model_name='pointage',
            name='Employe',
            field=models.ForeignKey(default='employe', on_delete=django.db.models.deletion.CASCADE, to='app1.employe'),
            preserve_default=False,
        ),
    ]
