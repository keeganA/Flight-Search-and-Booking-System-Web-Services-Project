# Generated by Django 3.2.17 on 2023-05-14 23:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0002_flight_instance_airline_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flight_instance',
            old_name='arrival_location',
            new_name='arrival_country',
        ),
        migrations.RenameField(
            model_name='flight_instance',
            old_name='departure_location',
            new_name='departure_country',
        ),
    ]
