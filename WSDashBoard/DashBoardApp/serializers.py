from rest_framework import serializers
from DashBoardApp.models import API, Mashup


class APISerializer(serializers.ModelSerializer):

    class Meta:
        model = API
        fields = ('uid',
                  'name')


class MashupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mashup
        fields = ('mid',
                  'name')
