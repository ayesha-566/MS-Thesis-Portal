# Generated by Django 3.2.7 on 2022-04-07 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Thesis', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='thesis',
            name='future_work',
            field=models.TextField(null=True),
        ),
    ]
