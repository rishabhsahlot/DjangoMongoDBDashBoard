import uuid
# from django.db import models
from djongo import models


# Create your models here.
class TextFieldWrapper(models.Model):
    text = models.TextField()

    class Meta:
        abstract = True


class API(models.Model):
    uid = models.URLField()
    title = models.TextField(blank=True, default='')
    summary = models.TextField(blank=False, default='')
    rating = models.FloatField()
    name = models.TextField(blank=False, default='')
    label = models.TextField()
    author = models.TextField()
    description = models.TextField()
    APIType = models.IntegerField()
    downloads = models.TextField()

    useCount = models.IntegerField()
    sampleUrl = models.URLField()
    downloadUrl = models.URLField()

    dateModified = models.DateTimeField()
    remoteFeed = models.TextField()
    numComments = models.IntegerField()
    commentsUrl = models.URLField()
    Tags = models.TextField()  # Array
    category = models.TextField()
    protocols = models.TextField()
    serviceEndpoint = models.URLField()
    version = models.FloatField()
    wsdl = models.URLField()
    data_formats = models.TextField()
    apigroups = models.TextField()
    example = models.TextField()
    clientInstall = models.TextField()  # models.BooleanField()
    authentication = models.TextField()
    ssl = models.TextField()  # models.BooleanField()
    readonly = models.TextField()
    VendorAPIKits = models.TextField()
    CommunityAPIKits = models.TextField()
    blog = models.URLField()
    forum = models.URLField()
    support = models.URLField()
    accountReq = models.TextField()  # models.BooleanField()
    commercial = models.TextField()
    provider = models.URLField()
    managedBy = models.TextField()
    nonCommercial = models.TextField()
    dataLicensing = models.TextField()
    fees = models.TextField()
    limits = models.TextField()
    terms = models.URLField()
    company = models.IntegerField()
    updated = models.DateTimeField()


class Mashup(models.Model):
    mid = models.URLField()
    title = models.TextField()
    summary = models.TextField()
    rating = models.FloatField()
    name = models.TextField()
    label = models.TextField()
    author = models.TextField()
    description = models.TextField()
    MashupType = models.TextField()
    downloads = models.IntegerField()
    useCount = models.IntegerField()
    sampleUrl = models.URLField()

    dateModified = models.DateTimeField()
    numComments = models.IntegerField()
    commentsUrl = models.URLField()
    Tags = models.TextField()  # models.ArrayField(model_container=TextFieldWrapper)
    APINames = models.TextField()  # models.ArrayField(model_container=TextFieldWrapper)
    APIURLs = models.TextField()  # models.ArrayField(model_container=TextFieldWrapper)

    updated = models.DateTimeField()
