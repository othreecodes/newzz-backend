# Generated by Django 2.0.9 on 2018-12-07 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0005_auto_20181207_0839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsitem',
            name='excerpt',
            field=models.TextField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='newsitem',
            name='title',
            field=models.TextField(max_length=250),
        ),
    ]
