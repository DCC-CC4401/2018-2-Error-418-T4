# Generated by Django 2.1.3 on 2018-11-21 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coevaluador', '0009_auto_20181121_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teammember',
            name='work_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wt_members', to='coevaluador.WorkTeam'),
        ),
    ]
