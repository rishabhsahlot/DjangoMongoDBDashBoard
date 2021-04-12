from django.shortcuts import render

# Create your views here.
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from WSDashBoard.DashBoardApp.models import API, Mashup
from WSDashBoard.DashBoardApp.serializers import APISerializer, MashupSerializer
from rest_framework.decorators import api_view

import pandas as pd
from datetime import datetime
import math


@api_view(['GET', 'DELETE'])
def APIList(request):
    # GET list of APIs, POST a new API, DELETE all API
    if request.method == 'GET':

        # Getting text file containing API information
        db_source = request.GET.get('DBSource', None)
        if db_source is None:
            apis = API.objects.all()

            # Updated year
            updatedyear = request.GET.get('updatedyear', None)
            if updatedyear is not None:
                apis = apis.filter(updated__year=updatedyear)

            # Protocols
            protocols = request.GET.get('protcols', None)
            if protocols is not None:
                protocols = protocols.split(',')
                for protocol in protocols:
                    protocol_regex = ".*" + protocol+".*"
                    apis = apis.filter(protocol__regex=protocol_regex)

            # Category
            category = request.GET.get('category', None)
            if category is not None:
                apis = apis.filter(category=category)

            # Rating
            rat = request.GET.get('category', None)
            if rat is not None:
                [op, rat] = rat.split("-")
                rat = float(rat)
                if op == 'lt':
                    apis = apis.filter(rating__lt=rat)
                elif op == 'gt':
                    apis = apis.filter(rating__gt=rat)
                else:
                    apis = apis.filter(rating=rat)

            # Tags
            tags = request.GET.get('Tags', None)
            if tags is not None:
                tags = tags.split(',')
                apis = apis.filter(Tags__all=tags)

            # Keywords
            keywords = request.GET.get('Keywords', None)
            if keywords is not None:
                keywords = keywords.split(",")
                for keyword in keywords:
                    keyword_regex = ".*" + keyword+".*"
                    apis = apis.filter(title__regex=keyword_regex)
                    apis = apis.filter(summary__regex=keyword_regex)
                    apis = apis.filter(description__regex=keyword_regex)

            apis_serializer = APISerializer(apis, many=True)
            return JsonResponse(apis_serializer.data, safe=False)

        else:
            apiCols = ['_id', 'title', 'summary', 'rating', 'name', 'label', 'author', 'description', 'APIType', 'downloads', 'useCount', 'sampleUrl',
                       'downloadUrl', 'dateModified', 'remoteFeed', 'numComments', 'commentsUrl', 'Tags', 'category', 'protocols', 'serviceEndpoint',
                       'version', 'wsdl', 'data_formats', 'apigroups', 'example', 'clientInstall', 'authentication', 'ssl', 'readonly',
                       'VendorApiKits', 'CommunityApiKits', 'blog', 'forum', 'support', 'accountReq', 'commercial', 'provider', 'managedBy',
                       'nonCommercial', 'dataLicensing', 'fees', 'limits', 'terms', 'company', 'updated']

            apiData = pd.read_csv('data/api.txt', sep="\$\#\$", names=apiCols)

            apiData['Tags'] = apiData['Tags'].apply(
                lambda x: x.split('###') if isinstance(x, str) else x)
            apiData['ssl'] = apiData['ssl'].apply(
                lambda x: x.capitalize() if isinstance(x, str) else x)
            apiData['accountReq'] = apiData['accountReq'].apply(
                lambda x: x.capitalize() if isinstance(x, str) else x)
            apiData['dateModified'] = apiData['dateModified'].apply(lambda x: datetime.strptime(
                x.replace('Z', 'UTC'), '%Y-%m-%dT%H:%M:%S%Z') if isinstance(x, str) else x)
            apiData['updated'] = apiData['updated'].apply(lambda x: datetime.strptime(
                x.replace('Z', 'UTC'), '%Y-%m-%dT%H:%M:%S%Z') if isinstance(x, str) else x)

            data = [{k: v for k, v in m.items() if not (isinstance(
                v, float) and math.isnan(v))} for m in apiData.to_dict(orient='rows')]

            aList = [API(**vals) for vals in data]

            API.objects.bulk_create(aList)

    elif request.method == 'DELETE':
        count = API.objects.all().delete()
        return JsonResponse({'message': '{} Mashups were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET',  'DELETE'])
def MashupList(request):
    # GET list of Mashups, POST a new Mashup Database, DELETE all Mashups
    if request.method == 'GET':

        # Getting text file containing API information
        db_source = request.GET.get('DBSource', None)
        if db_source is None:
            mashups = Mashup.objects.all()

            # Updated year
            updatedyear = request.GET.get('updatedyear', None)
            if updatedyear is not None:
                mashups = mashups.filter(updated__year=updatedyear)

            # Used APIs
            apis = request.GET.get('APIs', None)
            if apis is not None:
                apis = apis.split(',')
                mashups = mashups.filter(APINames__all=apis)

            # Tags
            tags = request.GET.get('Tags', None)
            if tags is not None:
                tags = tags.split(',')
                mashups = mashups.filter(Tags__all=tags)

            # Keywords
            keywords = request.GET.get('Keywords', None)
            if keywords is not None:
                keywords = keywords.split(",")
                for keyword in keywords:
                    keyword_regex = ".*" + keyword+".*"
                    mashups = mashups.filter(title__regex=keyword_regex)
                    mashups = mashups.filter(summary__regex=keyword_regex)
                    mashups = mashups.filter(description__regex=keyword_regex)

            mashups_serializer = MashupSerializer(mashups, many=True)
            return JsonResponse(mashups_serializer.data, safe=False)

        else:

            mashupCols = ['id', 'title', 'summary', 'rating', 'name', 'label', 'author', 'description', 'type', 'downloads', 'useCount', 'sampleUrl',
                          'dateModified', 'numComments', 'commentsUrl', 'Tags', 'APIs', 'updated']

            mashupData = pd.read_csv(
                db_source, sep="\$\#\$", names=mashupCols)  # 'data/mashup.txt'

            mashupData['Tags'] = mashupData['Tags'].apply(
                lambda x: x.split('###') if isinstance(x, str) else x)
            mashupData['APIs'] = mashupData['APIs'].apply(lambda x: list(
                map(lambda y: y.split('$$$'), x.split('###'))) if isinstance(x, str) else x)
            mashupData['APINames'] = mashupData['APIs'].apply(
                lambda x: list(map(lambda y: y[0], x)) if isinstance(x, list) else x)
            mashupData['APIURLs'] = mashupData['APIs'].apply(
                lambda x: list(map(lambda y: y[1], x)) if isinstance(x, list) else x)
            mashupData['dateModified'] = mashupData['dateModified'].apply(lambda x: datetime.strptime(
                x.replace('Z', 'UTC'), '%Y-%m-%dT%H:%M:%S%Z') if isinstance(x, str) else x)
            mashupData['updated'] = mashupData['updated'].apply(lambda x: datetime.strptime(
                x.replace('Z', 'UTC'), '%Y-%m-%dT%H:%M:%S%Z') if isinstance(x, str) else x)
            mashupData = mashupData.drop(columns=['APIs'])

            data = [{k: v for k, v in m.items() if not (isinstance(v, float) and math.isnan(v))}
                    for m in mashupData.to_dict(orient='rows')]

            aList = [Mashup(**vals) for vals in data]

            Mashup.objects.bulk_create(aList)

    elif request.method == 'DELETE':
        count = Mashup.objects.all().delete()
        return JsonResponse({'message': '{} Mashups were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
