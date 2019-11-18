# Generated by Django 2.0.6 on 2018-06-13 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('presentedId', models.IntegerField(default=-1)),
                ('engineId', models.IntegerField(default=-1)),
                ('binarySelections', models.CharField(max_length=200)),
                ('numSelected', models.IntegerField(default=-1)),
                ('likert', models.IntegerField(default=-1)),
                ('answeringTimeS', models.IntegerField(default=-1)),
            ],
        ),
        migrations.CreateModel(
            name='InterviewSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organisationPart', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='RandomisationOrders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('randomisationSeed', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='interviewsession',
            name='orderId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uiquery.RandomisationOrders'),
        ),
        migrations.AddField(
            model_name='answers',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uiquery.InterviewSession'),
        ),
    ]