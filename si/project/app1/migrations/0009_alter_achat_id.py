# Generated by Django 5.0.1 on 2024-01-20 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0008_alter_achat_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achat',
            name='id',
            field=models.IntegerField(auto_created=True, primary_key=True, serialize=False, unique=True),
        ),
    ]