# Generated by Django 4.2.7 on 2024-06-13 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theses_ci', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theses',
            name='fichier',
            field=models.FileField(blank=True, null=True, upload_to='theses/'),
        ),
    ]