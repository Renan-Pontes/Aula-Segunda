from rest_framework import serializers

from .models import CalculosDeJuros


class CalculosDeJurosSerializer(serializers.ModelSerializer):
     class Meta:
          model = CalculosDeJuros
          exclude = ['id']


class MesSerializer(serializers.Serializer):
     mes = serializers.IntegerField(min_value=1, max_value=12)


class CNPJSerializer(serializers.Serializer):
     cnpj = serializers.CharField()
