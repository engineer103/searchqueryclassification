# Generated by Django 2.1.1 on 2018-10-05 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20181005_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchtermsfile',
            name='classification_file',
            field=models.FileField(blank=True, null=True, upload_to='classification_files/'),
        ),
    ]
