from rest_framework import serializers

from .models import MyUser,Patient,HealthWorker,Request

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = MyUser
    fields = '__all__'
    extra_kwargs = {'password': {'write_only': True,
    'required': True}}

class PatientSerializer(serializers.ModelSerializer):
  class Meta:
    model = Patient
    fields = '__all__'

class HealthWorkerSerializer(serializers.ModelSerializer):
  class Meta:
    model = HealthWorker
    fields = '__all__'

class RequestSerializer(serializers.ModelSerializer):
  class Meta:
    model = Request
    fields = '__all__'
