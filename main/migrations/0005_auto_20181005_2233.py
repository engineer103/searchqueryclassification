# Generated by Django 2.1.1 on 2018-10-05 22:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20181005_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processingq',
            name='search_terms_file',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.SearchTermsFile'),
        ),
    ]
