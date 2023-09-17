from rest_framework import serializers
from timeseries.models import *

class seasonality_serializer(serializers.ModelSerializer):
    class Meta:
        model = seasonality_component
        fields = "__all__"

class configuration_serializer(serializers.ModelSerializer):
    seasonality = seasonality_serializer(many=True, read_only=True)
    class Meta:
        model = save_configuration
        fields = "__all__"
class timeseries_serializer(serializers.ModelSerializer):
    configuration=configuration_serializer(many=True,read_only=True)
    class Meta:
        model = simulator_details
        fields = "__all__"






