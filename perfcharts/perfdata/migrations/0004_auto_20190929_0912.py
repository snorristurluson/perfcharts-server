# Generated by Django 2.2.5 on 2019-09-29 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfdata', '0003_result_checksum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='benchmark',
            name='checksum',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='benchmark',
            name='description',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
