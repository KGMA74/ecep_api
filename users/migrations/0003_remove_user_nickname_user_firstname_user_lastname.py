# Generated by Django 5.1.6 on 2025-03-05 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_level_id_alter_level_level_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='nickname',
        ),
        migrations.AddField(
            model_name='user',
            name='firstname',
            field=models.CharField(default='firstname', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='lastname',
            field=models.CharField(default='lastname', max_length=50),
            preserve_default=False,
        ),
    ]
