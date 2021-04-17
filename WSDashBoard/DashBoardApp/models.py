import uuid
# from django.db import models
from djongo import models


# Create your models here.
class TextFieldWrapper(models.Model):
    text = models.TextField()

    class Meta:
        abstract = True


class API(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uid = models.URLField()
    title = models.TextField(blank=True, default='')
    summary = models.TextField(blank=False, default='')
    rating = models.FloatField()
    name = models.TextField(blank=False, default='')
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
    Tags = models.ArrayField(model_container=TextFieldWrapper)
    category = models.TextField()
    protocols = models.TextField()
    serviceEndpoint = models.URLField()
    version = models.FloatField()
    wsdl = models.URLField()
    data_formats = models.TextField()
    apigroups = models.TextField()
    example = models.TextField()
    clientInstall = models.BooleanField()  # models.TextField()
    authentication = models.TextField()
    ssl = models.BooleanField()  # models.TextField()
    readonly = models.TextField()
    VendorAPIKits = models.TextField()
    CommunityAPIKits = models.TextField()
    blog = models.URLField()
    forum = models.URLField()
    support = models.URLField()
    accountReq = models.BooleanField()  # models.TextField()
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    Tags = models.ArrayField(model_container=TextFieldWrapper)
    APINames = models.ArrayField(model_container=TextFieldWrapper)
    APIURLs = models.ArrayField(model_container=TextFieldWrapper)
    APIs = models.ArrayField(model_container=TextArrayFieldWrapper)

    updated = models.DateTimeField()
