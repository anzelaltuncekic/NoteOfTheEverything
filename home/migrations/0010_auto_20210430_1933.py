# Generated by Django 3.0 on 2021-04-30 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_note_newcomments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='newcomments',
        ),
        migrations.AddField(
            model_name='note',
            name='comment_count',
            field=models.IntegerField(default=0),
        ),
    ]
