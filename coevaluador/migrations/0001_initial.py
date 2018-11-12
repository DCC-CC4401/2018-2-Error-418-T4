# Generated by Django 2.1.3 on 2018-11-11 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('rut', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=35)),
                ('surname', models.CharField(max_length=35)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Coevaluation',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('n_questions', models.IntegerField()),
                ('status', models.CharField(max_length=50)),
                ('s_date', models.DateField()),
                ('e_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='CoevaluationSheet',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=100)),
                ('grade', models.FloatField()),
                ('coevaluation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coevaluador.Coevaluation')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=30)),
                ('year', models.IntegerField()),
                ('semester', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CourseRecordForStudent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.CharField(max_length=100)),
                ('coevaluation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coevaluador.Coevaluation')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coevaluador.Course')),
            ],
        ),
        migrations.CreateModel(
            name='NaturalPerson',
            fields=[
                ('rut', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('question', models.CharField(max_length=500)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coevaluador.Course')),
            ],
        ),
        migrations.CreateModel(
            name='TeachingTeamMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('password', models.CharField(max_length=50)),
                ('rol', models.CharField(max_length=100)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coevaluador.Course')),
            ],
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coevaluador.Student')),
            ],
        ),
        migrations.CreateModel(
            name='TeamRecordForStudent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coevaluador.Course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coevaluador.Student')),
            ],
        ),
        migrations.CreateModel(
            name='WorkTeam',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coevaluador.Course')),
            ],
        ),
        migrations.AddField(
            model_name='teamrecordforstudent',
            name='work_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coevaluador.WorkTeam'),
        ),
        migrations.AddField(
            model_name='teammember',
            name='work_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coevaluador.WorkTeam'),
        ),
        migrations.AddField(
            model_name='courserecordforstudent',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coevaluador.Student'),
        ),
        migrations.AddField(
            model_name='coevaluationsheet',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coevaluador.Course'),
        ),
        migrations.AddField(
            model_name='coevaluationsheet',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coevaluador.Student'),
        ),
        migrations.AddField(
            model_name='coevaluationsheet',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coevaluador.WorkTeam'),
        ),
        migrations.AddField(
            model_name='coevaluation',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coevaluador.Course'),
        ),
        migrations.AddField(
            model_name='answer',
            name='coevaluation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coevaluador.Coevaluation'),
        ),
        migrations.AddField(
            model_name='answer',
            name='evaluated',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluated', to='coevaluador.Student'),
        ),
        migrations.AddField(
            model_name='answer',
            name='evaluator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluator', to='coevaluador.Student'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coevaluador.Question'),
        ),
    ]
