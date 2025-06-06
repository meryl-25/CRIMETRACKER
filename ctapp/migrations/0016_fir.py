# Generated by Django 5.0 on 2025-03-20 17:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ctapp', '0015_crime_latitude_crime_longitude_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FIR',
            fields=[
                ('fir_id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('witness_details', models.TextField()),
                ('evidence_details', models.TextField()),
                ('crime_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ctapp.crime')),
            ],
            options={
                'db_table': 'tbl_fir',
            },
        ),
    ]
