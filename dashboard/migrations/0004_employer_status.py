# Generated by Django 3.2.9 on 2021-11-15 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_auto_20211114_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='employer',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]