# Generated by Django 3.1.14 on 2022-07-18 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('francoralite_api', '0006_add_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='url_file',
            field=models.URLField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='file',
            field=models.FileField(blank=True, db_column='filename', max_length=1024, null=True, upload_to='items', verbose_name='fichier son'),
        ),
    ]
