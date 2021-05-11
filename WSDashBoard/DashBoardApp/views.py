from django.shortcuts import render

# Create your views here.
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from DashBoardApp.models import API, Mashup
from DashBoardApp.serializers import APISerializer, MashupSerializer
from rest_framework.decorators import api_view

import pandas as pd
from datetime import datetime
import math
from tqdm import tqdm

import itertools


@api_view(['GET'])
def getCounts(request):

    # APIs = API.objects.all()
    categories = list(set(API.objects.values_list('category', flat=True)))
    categories = list(
        map(lambda x: {'key': x, 'text': x, 'value': x}, categories))
    api_tags = list(map(lambda x: x.split(','), list(
        API.objects.values_list('Tags', flat=True))))
    api_tags = list(set(list(itertools.chain.from_iterable(api_tags))))
    api_tags = list(map(lambda x: {'key': x, 'text': x, 'value': x}, api_tags))
    protocols = list(set(API.objects.values_list('protocols', flat=True)))
    protocols = list(
        map(lambda x: {'key': x, 'text': x, 'value': x}, protocols))

    api_updated = list(set(API.objects.values_list('updated', flat=True)))
    api_years = list(map(lambda x: {'key': x, 'text': x, 'value': x}, set(
        map(lambda x: x.year, api_updated))))

    API_data = {'categories': categories, 'api_tags': api_tags,
                'protocols': protocols, 'years': api_years}

    mashup_tags = list(map(lambda x: x.split(','), list(
        Mashup.objects.values_list('Tags', flat=True))))
    mashup_tags = list(set(list(itertools.chain.from_iterable(mashup_tags))))
    mashup_tags = list(
        map(lambda x: {'key': x, 'text': x, 'value': x}, mashup_tags))

    mashup_apinames = list(map(lambda x: x.split(','), list(
        Mashup.objects.values_list('APINames', flat=True))))
    mashup_apinames = list(
        set(list(itertools.chain.from_iterable(mashup_apinames))))
    mashup_apinames = list(
        map(lambda x: {'key': x, 'text': x, 'value': x}, mashup_apinames))

    mashup_updated = list(
        set(Mashup.objects.values_list('updated', flat=True)))
    mashup_years = list(map(lambda x: {'key': x, 'text': x, 'value': x}, set(
        map(lambda x: x.year, mashup_updated))))

    Mashup_data = {'tags': mashup_tags,
                   'apinames': mashup_apinames, 'years': mashup_years}

    response = {'APICount': API.objects.all().count(), 'MashupCount': Mashup.objects.all(
    ).count(), 'API': API_data, 'Mashup': Mashup_data}
    return JsonResponse(response)


@api_view(['GET'])
def deleteAPIs(request):
    count = API.objects.all().count()
    API.objects.all().delete()
    return JsonResponse({'message': '{} APIs were deleted successfully!'.format(count)}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def deleteMashups(request):
    count = Mashup.objects.all().count()
    Mashup.objects.all().delete()
    return JsonResponse({'message': '{} Mashups were deleted successfully!'.format(count)}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def APIList(request):
    # GET list of APIs, POST a new API, DELETE all API
    if request.method == 'GET':
        countflag = request.GET.get('CountRequest', None)
        if countflag is not None:
            return JsonResponse({'count': API.objects.all().count()})

        # Getting text file containing API information
        db_source = request.GET.get('DBSource', None)
        if db_source is None:
            apis = API.objects.all()

            # Updated year
            updatedyear = request.GET.get('updatedyear', None)
            if updatedyear is not None:
                apis = apis.filter(updated__year=updatedyear)

            # Protocols
            protocols = request.GET.get('protocols', None)
            if protocols is not None:
                protocols = protocols.replace('%20', ' ')
                protocols = protocols.split(',')
                for protocol in protocols:
                    apis = apis.filter(protocols__icontains=protocol)

            # Category
            category = request.GET.get('category', None)
            if category is not None:
                apis = apis.filter(category=category)

            # Rating
            rat = request.GET.get('rating', None)
            if rat is not None:
                [rat, op] = rat.split("-")
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
                tags = tags.replace('%20', ' ')
                tags = tags.split(',')
                for tag in tags:
                    apis = apis.filter(Tags__icontains=tag)

                # apis = apis.filter(Tags__all=tags)

            # Keywords
            keywords = request.GET.get('Keywords', None)
            if keywords is not None:
                keywords = keywords.replace('%20', ' ')
                keywords = keywords.split(",")
                for keyword in keywords:
                    apis = apis.filter(title__icontains=keyword)
                    apis = apis.filter(summary__icontains=keyword)
                    apis = apis.filter(description__icontains=keyword)

            apis = apis.values(
                'name', 'uid')
            apis_serializer = APISerializer(apis, many=True)
            return JsonResponse(apis_serializer.data, safe=False)

        else:
            apiCols = ['uid', 'title', 'summary', 'rating', 'name', 'label', 'author', 'description', 'APIType', 'downloads', 'useCount', 'sampleUrl',
                       'downloadUrl', 'dateModified', 'remoteFeed', 'numComments', 'commentsUrl', 'Tags', 'category', 'protocols', 'serviceEndpoint',
                       'version', 'wsdl', 'data_formats', 'apigroups', 'example', 'clientInstall', 'authentication', 'ssl', 'readonly',
                       'VendorAPIKits', 'CommunityAPIKits', 'blog', 'forum', 'support', 'accountReq', 'commercial', 'provider', 'managedBy',
                       'nonCommercial', 'dataLicensing', 'fees', 'limits', 'terms', 'company', 'updated']
            print(db_source)
            apiData = pd.read_csv(db_source, sep="\$\#\$", names=apiCols)
            #  len(apiData))
            apiData['Tags'] = apiData['Tags'].apply(
                lambda x: ','.join(x.split('###')) if isinstance(x, str) else x)
            apiData['ssl'] = apiData['ssl'].apply(
                lambda x: x.capitalize() if isinstance(x, str) else x)
            apiData['accountReq'] = apiData['accountReq'].apply(
                lambda x: x.capitalize() if isinstance(x, str) else x)
            apiData['dateModified'] = apiData['dateModified'].apply(lambda x: datetime.strptime(
                x.replace('Z', 'UTC'), '%Y-%m-%dT%H:%M:%S%Z') if isinstance(x, str) else x)
            apiData['updated'] = apiData['updated'].apply(lambda x: datetime.strptime(
                x.replace('Z', 'UTC'), '%Y-%m-%dT%H:%M:%S%Z') if isinstance(x, str) else x)

            # tags = apiData['Tags'].apply(lambda x: x.split(',')).tolist()
            # tags = list(set(list(itertools.chain.from_iterable(tags))))
            # tags = list(map(lambda x: {'key': x, 'text': x, 'value': x}, tags))
            # protocols = list(map(lambda x: {'key': x, 'text': x, 'value': x}, list(
            #     apiData['protocols'].unique())))
            # categories = list(map(lambda x: {'key': x, 'text': x, 'value': x}, list(
            #     apiData['category'].unique())))
            # years = list(map(lambda x: {'key': x, 'text': x, 'value': x}, apiData['updated'].apply(
            #     lambda x: x.year).unique()))

            # response = {'api_record_count': len(apiData), 'protocols': protocols,
            #             'categories': categories, 'years': years}

            data = [{k: v for k, v in m.items() if not (isinstance(
                v, float) and math.isnan(v))} for m in apiData.to_dict(orient='rows')]

            aList = [API(**vals) for vals in data]
            del data

            for i in tqdm(range(len(aList))):
                aList[i].save()

            return JsonResponse({'Message': 'Successful'}, status=status.HTTP_201_CREATED)

            # /api/DashBoardApp/APIs?DBSource=D:\CoursesAndLearning\Spring2021\CSCI724\Assn3\DjangoMongoDBDashBoard\data\api.txt

    # elif request.method == 'DELETE':
    #     count = API.objects.all().delete()
    #     return JsonResponse({'message': '{} Mashups were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
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
            apis = request.GET.get('APINames', None)
            if apis is not None:
                apis = apis.replace('%20', ' ')
                apis = apis.split(',')
                print(apis)
                for api in apis:
                    # api_regex = r".*" + api+".*"
                    mashups = mashups.filter(APINames__icontains=api)

            # Tags
            tags = request.GET.get('Tags', None)
            if tags is not None:
                tags = tags.replace('%20', ' ')
                tags = tags.split(',')
                for tag in tags:
                    mashups = mashups.filter(Tags__icontains=tag)

            # Keywords
            keywords = request.GET.get('Keywords', None)
            if keywords is not None:
                keywords = keywords.replace('%20', ' ')
                keywords = keywords.split(",")
                for keyword in keywords:
                    # keyword_regex = ".*" + keyword+".*"
                    mashups = mashups.filter(title__icontains=keyword)
                    mashups = mashups.filter(summary__icontains=keyword)
                    mashups = mashups.filter(description__icontains=keyword)
            mashups = mashups.values('name', 'mid')
            mashups_serializer = MashupSerializer(mashups, many=True)
            return JsonResponse(mashups_serializer.data, safe=False)

        else:

            mashupCols = ['mid', 'title', 'summary', 'rating', 'name', 'label', 'author', 'description', 'type', 'downloads', 'useCount', 'sampleUrl',
                          'dateModified', 'numComments', 'commentsUrl', 'Tags', 'APIs', 'updated']

            mashupData = pd.read_csv(
                db_source, sep="\$\#\$", names=mashupCols)  # 'data/mashup.txt'

            mashupData['Tags'] = mashupData['Tags'].apply(
                lambda x: ','.join(x.split('###')) if isinstance(x, str) else x)
            mashupData['APIs'] = mashupData['APIs'].apply(lambda x: list(
                map(lambda y: y.split('$$$'), x.split('###'))) if isinstance(x, str) else x)
            mashupData['APINames'] = mashupData['APIs'].apply(
                lambda x: ','.join(list(map(lambda y: y[0], x))) if isinstance(x, list) else x)
            mashupData['APIURLs'] = mashupData['APIs'].apply(
                lambda x: ','.join(list(map(lambda y: y[1], x))) if isinstance(x, list) else x)
            mashupData['dateModified'] = mashupData['dateModified'].apply(lambda x: datetime.strptime(
                x.replace('Z', 'UTC'), '%Y-%m-%dT%H:%M:%S%Z') if isinstance(x, str) else x)
            mashupData['updated'] = mashupData['updated'].apply(lambda x: datetime.strptime(
                x.replace('Z', 'UTC'), '%Y-%m-%dT%H:%M:%S%Z') if isinstance(x, str) else x)
            mashupData = mashupData.drop(columns=['APIs'])

            # tags = mashupData['Tags'].apply(lambda x: x.split(',')).tolist()
            # tags = list(set(list(itertools.chain.from_iterable(tags))))
            # tags = list(map(lambda x: {'key': x, 'text': x, 'value': x}, tags))

            # apinames = mashupData['APINames'].apply(
            #     lambda x: x.split(',')).tolist()
            # apinames = list(set(list(itertools.chain.from_iterable(apinames))))
            # apinames = list(
            #     map(lambda x: {'key': x, 'text': x, 'value': x}, apinames))

            # years = list(map(lambda x: {'key': x, 'text': x, 'value': x}, mashupData['updated'].apply(
            #     lambda x: x.year).unique()))

            # response = {'tags': tags, 'apinames': apinames, 'years': years}

            data = [{k: v for k, v in m.items() if not (isinstance(v, float) and math.isnan(v))}
                    for m in mashupData.to_dict(orient='rows')]

            aList = [Mashup(**vals) for vals in data]

            del data
            for i in tqdm(range(len(aList))):
                aList[i].save()

            return JsonResponse({'Message': 'Successful'}, status=status.HTTP_201_CREATED)

    # elif request.method == 'DELETE':
    #     count = Mashup.objects.all().delete()
    #     return JsonResponse({'message': '{} Mashups were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
