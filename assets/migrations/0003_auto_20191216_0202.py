# Generated by Django 2.2.6 on 2019-12-16 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0002_auto_20191215_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documententry',
            name='file',
            field=models.URLField(),
        ),
    ]
