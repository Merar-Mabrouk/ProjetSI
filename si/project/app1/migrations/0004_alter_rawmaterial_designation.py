# Generated by Django 5.0.1 on 2024-01-20 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_alter_supplier_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawmaterial',
            name='designation',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
