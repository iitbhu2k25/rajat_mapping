# Generated by Django 5.1.6 on 2025-02-16 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stp", "0002_state_district_sub_district_villages"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sub_district",
            name="subdistrict_name",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="villages",
            name="village_name",
            field=models.CharField(max_length=100),
        ),
    ]
