# Generated by Django 3.2.12 on 2022-02-07 03:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zymo_api.country')),
            ],
            options={
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='CovidStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirmed', models.BigIntegerField(max_length=20)),
                ('recovered', models.BigIntegerField(max_length=20)),
                ('deaths', models.BigIntegerField()),
                ('population', models.BigIntegerField(blank=True, max_length=20, null=True)),
                ('sq_km_area', models.BigIntegerField(blank=True, null=True)),
                ('life_expectancy', models.CharField(blank=True, max_length=20, null=True)),
                ('elevation_in_meters', models.CharField(blank=True, max_length=10, null=True)),
                ('continent', models.CharField(blank=True, max_length=100, null=True)),
                ('abbreviation', models.CharField(blank=True, max_length=4, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('iso', models.IntegerField(blank=True, null=True)),
                ('capital_city', models.CharField(blank=True, max_length=200, null=True)),
                ('lat', models.CharField(blank=True, max_length=30, null=True)),
                ('long', models.CharField(blank=True, max_length=30, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zymo_api.country')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='zymo_api.region')),
            ],
        ),
        migrations.AddConstraint(
            model_name='country',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_name'),
        ),
        migrations.AddConstraint(
            model_name='region',
            constraint=models.UniqueConstraint(fields=('name', 'country'), name='unique_country_region_name'),
        ),
        migrations.AddConstraint(
            model_name='covidstats',
            constraint=models.UniqueConstraint(fields=('country', 'region'), name='unique_country_region'),
        ),
    ]
