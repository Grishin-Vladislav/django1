from rest_framework.serializers import ModelSerializer, CharField, \
    IntegerField
from .models import Sensor, Measurement


class SensorSerializer(ModelSerializer):
    description = CharField(required=True)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description']


class MeasurementSerializer(ModelSerializer):
    sensor_id = IntegerField(required=True)

    class Meta:
        model = Measurement
        fields = ['sensor_id', 'temperature', 'date']


class DetailedSensorSerializer(ModelSerializer):
    measurements = MeasurementSerializer(read_only=True, many=True)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements']
