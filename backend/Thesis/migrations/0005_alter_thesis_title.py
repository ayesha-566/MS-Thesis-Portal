# Generated by Django 3.2.7 on 2022-06-21 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Thesis', '0004_rename_conferences_conference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thesis',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
