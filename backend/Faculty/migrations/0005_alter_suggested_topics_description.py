# Generated by Django 3.2.7 on 2022-04-10 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Faculty', '0004_suggested_topics_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suggested_topics',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
