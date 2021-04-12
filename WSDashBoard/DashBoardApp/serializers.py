from rest_framework import serializers
from WSDashBoard.DashBoardApp.models import API, Mashup


class APISerializer(serializers.ModelSerializer):

    class Meta:
        model = API
        fields = ('_id',
                  'name'
                  'updated',
                  'protocols',
                  'category',
                  'rating',
                  'Tags',
                  'title',
                  'summary',
                  'description'
                  )


class MashupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mashup
        fields = ('_id',
                  'title',
                  'APIs',
                  'Tags'
                  'title',
                  'summary',
                  'description')
