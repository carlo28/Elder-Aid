# Generated by Django 4.1.5 on 2023-01-02 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=120)),
                ('participating_users', models.CharField(max_length=120)),
                ('time', models.DateTimeField()),
                ('activity', models.CharField(max_length=120)),
                ('active', models.BooleanField()),
                ('is_private', models.BooleanField()),
            ],
        ),
    ]