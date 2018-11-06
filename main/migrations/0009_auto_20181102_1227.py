# Generated by Django 2.1.1 on 2018-11-02 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20181005_2322'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='processingq',
            name='search_terms_file',
        ),
        migrations.RemoveField(
            model_name='searchtermsfile',
            name='classification_file',
        ),
        migrations.RemoveField(
            model_name='searchtermsfile',
            name='dictionary',
        ),
        migrations.AddField(
            model_name='processingq',
            name='classification_file',
            field=models.FileField(blank=True, null=True, upload_to='classification_files/'),
        ),
        migrations.AddField(
            model_name='processingq',
            name='dictionary',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Dictionary'),
        ),
        migrations.AddField(
            model_name='processingq',
            name='search_terms_file_new',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='search_terms_file_new', to='main.SearchTermsFile'),
        ),
        migrations.AddField(
            model_name='processingq',
            name='search_terms_file_organic',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='search_terms_file_organic', to='main.SearchTermsFile'),
        ),
        migrations.AddField(
            model_name='processingq',
            name='search_terms_file_paid',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='search_terms_file_paid', to='main.SearchTermsFile'),
        ),
    ]