# Generated by Django 5.1.6 on 2025-02-16 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stp", "0003_alter_sub_district_subdistrict_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sub_district",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
