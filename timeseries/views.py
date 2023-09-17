import pandas as pd
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.response import Response
from sklearn.preprocessing import MinMaxScaler
import random
from django.views.decorators.csrf import ensure_csrf_cookie

from datetime import datetime
from Seasonality import daily_seasonality, weekly_seasonality
from timeseries.models import *
from .Serializers import *
from rest_framework.decorators import action
from Seasonality.daily_seasonality import Daily_Seasonality
from Seasonality.weekly_seasonality import Weekly_Seasonality
from .models import *
from Cycles_and_trends.cycle import cycle
from Cycles_and_trends.trends import trends

from Generator.Time_Series import Time_Series
from Noise.missing_values import missing_values
from Noise.noise import noise
from Noise.outliers import outliers
from Save.csv_file import csv_file
# Create your views here.
class simulator(ListCreateAPIView, UpdateAPIView):
    queryset = simulator_details.objects.all()
    serializer_class = timeseries_serializer

    def create(self, request, *args, **kwargs):
        data=request.data
        ts_serial = timeseries_serializer(data=data)
        configuration=data.pop('configuration')[0]
        seaonality=configuration.pop('seasonality')[0]
        #ts_serial=timeseries_serializer(data=data)
        if ts_serial.is_valid():
            ts_serial.save()
        configurationserializer=configuration_serializer(data=configuration)
        if configurationserializer.is_valid():
            configurationserializer.save()
        seasonalityserializer=seasonality_serializer(data=seaonality)
        if seasonalityserializer.is_valid():
            seasonalityserializer.save()


        return Response("Time series added",status=200)






    @action(detail=True, methods=['GET'])

    def run(self,request,*args, **kwargs):
        id = request.Get.get('id',-1)

        data = simulator_details.objects.filter(id=id)[0]

        #ts_serial = timeseries_serializer(data=data)
        configuration = data.pop('configuration')[0]
        seaonality = configuration.pop('seasonality')[0]
        Start_date = data["start_date"]
        End_date = data["end_date"]
        use_case_name = data['use_case_name']
        frequencies = configuration["Frequency"]

        frequency_type = seaonality["frequency_type"]
        phase_shift = seaonality["phase_shift"]
        amplitude = seaonality["amplitude"]
        noise_levels = [configuration["Noise_level"]]
        trend_levels = [configuration["Trend_coefficient"]]
        cyclic_periods = [configuration["Cycle_frequency"]]
        data_types = data["time_series_type"]
        percentage_outliers_options = [configuration["Outlier_percentage"]]
        Start_date = datetime.strptime(Start_date, "%Y-%m-%d")
        End_date = datetime.strptime(End_date, "%Y-%m-%d")
        data_size = (End_date - Start_date).days
        counter = 0
        meta_data = []
        for noise_level in noise_levels:
            for trend in trend_levels:
                for cyclic_period in cyclic_periods:
                    for percentage_outliers in percentage_outliers_options:
                        for data_type in data_types:
                            for _ in range(13):

                                counter += 1

                                # Generate time index

                                series = Time_Series(Start_date, End_date, frequencies)
                                date_rng = series.create_time_series()
                                daily_seasonal_component = 1
                                weekly_seasonal_component = 1
                                # Create components
                                if frequency_type == "Daily":

                                    Daily_seasonality = Daily_Seasonality()
                                    daily_seasonal_component = Daily_seasonality.add_daily_seasonality(date_rng)
                                elif frequency_type == "Weekly":
                                    Weekly_seasonality = Weekly_Seasonality()
                                    weekly_seasonal_component = Weekly_seasonality.add_weekly_seasonality(date_rng)
                                trnd = trends(trend, data_size=data_size,
                                              data_type=data_type)
                                trend_component = trnd.add_trend(date_rng)
                                cyclic_period = "exist"
                                Cycle = cycle(cyclic_period, season_type=data_type)
                                cyclic_component = Cycle.add_cycles(date_rng)

                                # Combine components and add missing values and outliers
                                if data_type == 'multiplicative':
                                    data = daily_seasonal_component * weekly_seasonal_component * trend_component * cyclic_component
                                else:
                                    data = daily_seasonal_component + weekly_seasonal_component + trend_component + cyclic_component
                                    # Create a MinMaxScaler instance
                                    scaler = MinMaxScaler(feature_range=(-1, 1))
                                    data = scaler.fit_transform(data.values.reshape(-1, 1))
                                    Noise = noise(noise_level)
                                    data = Noise.add_noise(data)
                                    Outliers = outliers(percentage_outliers)
                                    data, anomaly = Outliers.add_outliers(data)
                                    Missing_Value = missing_values(0.05)
                                    data = Missing_Value.add_missing_values(data)
                                    df = pd.DataFrame({'value': data, 'timestamp': date_rng, 'anomaly': anomaly})
                                    file = csv_file('sample_datasets/' + str(counter) + '.csv', df)
                                    file.save()
                                    meta_data.append({'id': str(counter) + '.csv',
                                                      'data_type': data_type,
                                                      'daily_seasonality': daily_seasonality,
                                                      'weekly_seasonality': weekly_seasonality,
                                                      'noise (high 30% - low 10%)': noise_level,
                                                      'trend': trend,
                                                      'cyclic_period (3 months)': cyclic_period,

                                                      'percentage_outliers': percentage_outliers,
                                                      'percentage_missing': 0.05,
                                                      'freq': frequencies})
                                    # generate_csv(list(zip(date_rng, data)), file_name)

                                    meta_data_df = pd.DataFrame.from_records(meta_data)
                                    meta_data_file = csv_file('sample_datasets/meta_data.csv', meta_data_df)
                                    meta_data_file.save()

        return Response("Time series created",status=200)

    @action(detail=True, methods=['GET'])
    def stop(self,request):
        self.get_object()
        return




