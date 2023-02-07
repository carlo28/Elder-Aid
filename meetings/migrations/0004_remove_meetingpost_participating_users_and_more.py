# Generated by Django 4.1.5 on 2023-02-04 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0003_meetingpost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meetingpost',
            name='participating_users',
        ),
        migrations.AlterField(
            model_name='meetingpost',
            name='active',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='meetingpost',
            name='is_private',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
