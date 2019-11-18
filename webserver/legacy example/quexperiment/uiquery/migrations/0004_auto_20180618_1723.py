# Generated by Django 2.0.6 on 2018-06-18 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('uiquery', '0003_auto_20180616_0934'),
    ]

    operations = [
        migrations.CreateModel(
            name='RandomisationOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('presentOrder', models.IntegerField(default=-1)),
                ('searchtype', models.IntegerField(default=-1)),
                ('typeOrder', models.IntegerField(default=-1)),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uiquery.InterviewSession')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='query',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='uiquery.Query'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='query',
            name='query',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='randomisationorder',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uiquery.Query'),
        ),
    ]
