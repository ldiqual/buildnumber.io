from rest_framework import serializers

from models import *

class BuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Build
        fields = ('build_number',)

class AccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
