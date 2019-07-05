# Generated by Django 2.0.9 on 2018-12-07 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0003_auto_20181128_1959'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='site',
            options={'verbose_name': 'Site to Crawl', 'verbose_name_plural': 'Sites to Crawl'},
        ),
        migrations.AddField(
            model_name='newsitem',
            name='excerpt',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='newsitem',
            name='media_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='newsitem',
            name='url',
            field=models.URLField(default='', unique=True),
            preserve_default=False,
        ),
    ]