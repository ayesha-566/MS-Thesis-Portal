# Generated by Django 3.2.7 on 2022-04-02 06:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Faculty', '0001_initial'),
        ('Student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('domain_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='Thesis',
            fields=[
                ('thesis_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=600)),
                ('grade', models.CharField(max_length=4, null=True)),
                ('type', models.IntegerField()),
                ('year', models.IntegerField()),
                ('abstract', models.TextField(null=True)),
                ('thesis_file', models.FileField(null=True, upload_to='Thesis_Files/')),
                ('advisor_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Faculty.faculty')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Student.student')),
            ],
        ),
        migrations.CreateModel(
            name='DomainInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Thesis.domain')),
                ('thesis_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Thesis.thesis')),
            ],
        ),
    ]
