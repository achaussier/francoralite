# Generated by Django 3.1.14 on 2022-09-07 05:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('francoralite_api', '0007_item_add_url_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='domain',
            field=models.CharField(blank=True, max_length=5, verbose_name='Domaine'),
        ),
    ]
