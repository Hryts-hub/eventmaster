# Generated by Django 3.1.5 on 2021-02-13 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20210208_1226'),
    ]

    operations = [
        migrations.AddField(
            model_name='holidays',
            name='updated',
            field=models.BooleanField(default=True),
        ),
    ]
