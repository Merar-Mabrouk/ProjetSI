# Generated by Django 5.0.1 on 2024-01-20 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_alter_rawmaterial_qstock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='last_name',
            field=models.CharField(max_length=40, unique=True),
        ),
    ]
