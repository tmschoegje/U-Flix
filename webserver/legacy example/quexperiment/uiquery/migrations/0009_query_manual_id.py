# Generated by Django 2.0.6 on 2018-06-19 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uiquery', '0008_remove_answer_query'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='manual_id',
            field=models.IntegerField(default=-1),
        ),
    ]
