# Generated by Django 2.2.5 on 2019-09-28 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('perfdata', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='benchmark',
            name='checksum',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AddField(
            model_name='benchmark',
            name='executable',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='benchmarks', to='perfdata.Executable'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='benchmark',
            name='reference',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='benchmarks', to='perfdata.Revision'),
        ),
        migrations.AlterField(
            model_name='benchmark',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='benchmark',
            unique_together={('name', 'executable')},
        ),
    ]