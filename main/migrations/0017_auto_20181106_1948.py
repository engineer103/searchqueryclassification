# Generated by Django 2.1.3 on 2018-11-06 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20181106_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchclassification',
            name='query',
            field=models.CharField(blank=True, max_length=1020),
        ),
        migrations.AlterField(
            model_name='searchclassification',
            name='search_dictionary_ids',
            field=models.CharField(blank=True, max_length=1020),
        ),
    ]
