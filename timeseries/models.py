from django.db import models

# Create your models here.
class simulator_details(models.Model):
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    use_case_name=models.CharField(max_length=30)
    time_series_type=models.CharField(max_length=14)
    producer_type = models.CharField(max_length=30)
class save_configuration(models.Model):
    Frequency=models.CharField(max_length=10)
    Noise_level=models.FloatField(max_length=10)
    Trend_coefficient=models.FloatField(max_length=10,default='0')
    Missing_percentage=models.FloatField(default=0)
    Outlier_percentage = models.FloatField(default=0)
    Cycle_amplitude=models.FloatField(default=0)
    Cycle_frequency=models.FloatField(default=0)
    details=models.ForeignKey(simulator_details,on_delete=models.CASCADE,related_name="configuration")
class seasonality_component(models.Model):
    amplitude=models.FloatField()
    phase_shift=models.FloatField()
    frequency_type=models.CharField(max_length=10)
    frequency_multiplier=models.FloatField()
    configuration=models.ForeignKey(save_configuration,on_delete=models.CASCADE,related_name="seasonality")



