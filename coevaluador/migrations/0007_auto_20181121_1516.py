# Generated by Django 2.1.3 on 2018-11-21 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coevaluador', '0006_auto_20181121_1445'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='evaluated',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='evaluator',
        ),
    ]
