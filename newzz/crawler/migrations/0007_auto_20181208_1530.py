# Generated by Django 2.0.9 on 2018-12-08 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0006_auto_20181207_0852'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsitem',
            name='sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='newsitem',
            name='excerpt',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='newsitem',
            name='title',
            field=models.TextField(),
        ),
    ]
