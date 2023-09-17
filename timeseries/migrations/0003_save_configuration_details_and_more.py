# Generated by Django 4.2.5 on 2023-09-12 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("timeseries", "0002_seasonality_component"),
    ]

    operations = [
        migrations.AddField(
            model_name="save_configuration",
            name="details",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="timeseries.simulator_details",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="save_configuration",
            name="Missing_percentage",
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name="save_configuration",
            name="Outlier_percentage",
            field=models.FloatField(default=0),
        ),
    ]
