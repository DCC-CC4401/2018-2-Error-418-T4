# Generated by Django 2.1.3 on 2018-11-18 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coevaluador', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coevaluation',
            name='e_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='coevaluation',
            name='s_date',
            field=models.DateTimeField(),
        ),
    ]
