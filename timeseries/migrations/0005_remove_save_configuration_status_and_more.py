# Generated by Django 4.2.5 on 2023-09-14 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        (
            "timeseries",
            "0004_remove_save_configuration_cycle_component_amplitude_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="save_configuration",
            name="Status",
        ),
        migrations.AddField(
            model_name="save_configuration",
            name="Cycle_amplitude",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="save_configuration",
            name="Cycle_frequency",
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name="save_configuration",
            name="Noise_level",
            field=models.FloatField(max_length=10),
        ),
        migrations.AlterField(
            model_name="save_configuration",
            name="Trend_coefficient",
            field=models.FloatField(default="0", max_length=10),
        ),
        migrations.AlterField(
            model_name="save_configuration",
            name="details",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="configuration",
                to="timeseries.simulator_details",
            ),
        ),
        migrations.AlterField(
            model_name="seasonality_component",
            name="configuration",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="seasonality",
                to="timeseries.save_configuration",
            ),
        ),
    ]
