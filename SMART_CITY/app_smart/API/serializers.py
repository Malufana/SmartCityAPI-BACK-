from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from app_smart.models import Sensor, TemperaturaData, UmidadeData, LuminosidadeData, ContadorData

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


# class CreateSensorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Sensor
#         fields = ['id', 'tipo', 'mac_address', 'latitude', 'longitude', 'localizacao', 'responsavel', 'unidade_medida', 'status_operacional', 'observacao']

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'

class CSVFileUploadSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)

class TemperaturaDataSerliazer(serializers.ModelSerializer):
    sensor_id = serializers.PrimaryKeyRelatedField(source='sensor', read_only=True)
    class Meta:
        model = TemperaturaData
        fields = '__all__'

class UmidadeDataSerializer(serializers.ModelSerializer):
    sensor_id = serializers.PrimaryKeyRelatedField(source='sensor', read_only=True)
    class Meta:
        model = UmidadeData
        fields = '__all__'

class LuminosidadeDataSerializer(serializers.ModelSerializer):
    sensor_id = serializers.PrimaryKeyRelatedField(source='sensor', read_only=True)
    class Meta:
        model = LuminosidadeData
        fields = '__all__'

class ContadorDataSerializer(serializers.ModelSerializer):
    sensor_id = serializers.PrimaryKeyRelatedField(source='sensor', read_only=True)
    class Meta:
        model = ContadorData
        fields = '__all__'