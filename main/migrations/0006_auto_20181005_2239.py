# Generated by Django 2.1.1 on 2018-10-05 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20181005_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processingq',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
