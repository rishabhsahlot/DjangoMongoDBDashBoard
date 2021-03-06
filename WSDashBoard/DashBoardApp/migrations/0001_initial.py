# Generated by Django 3.0.5 on 2021-04-25 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='API',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.URLField()),
                ('title', models.TextField(blank=True, default='')),
                ('summary', models.TextField(default='')),
                ('rating', models.FloatField()),
                ('name', models.TextField(default='')),
                ('label', models.TextField()),
                ('author', models.TextField()),
                ('description', models.TextField()),
                ('APIType', models.IntegerField()),
                ('downloads', models.TextField()),
                ('useCount', models.IntegerField()),
                ('sampleUrl', models.URLField()),
                ('downloadUrl', models.URLField()),
                ('dateModified', models.DateTimeField()),
                ('remoteFeed', models.TextField()),
                ('numComments', models.IntegerField()),
                ('commentsUrl', models.URLField()),
                ('Tags', models.TextField()),
                ('category', models.TextField()),
                ('protocols', models.TextField()),
                ('serviceEndpoint', models.URLField()),
                ('version', models.FloatField()),
                ('wsdl', models.URLField()),
                ('data_formats', models.TextField()),
                ('apigroups', models.TextField()),
                ('example', models.TextField()),
                ('clientInstall', models.TextField()),
                ('authentication', models.TextField()),
                ('ssl', models.TextField()),
                ('readonly', models.TextField()),
                ('VendorAPIKits', models.TextField()),
                ('CommunityAPIKits', models.TextField()),
                ('blog', models.URLField()),
                ('forum', models.URLField()),
                ('support', models.URLField()),
                ('accountReq', models.TextField()),
                ('commercial', models.TextField()),
                ('provider', models.URLField()),
                ('managedBy', models.TextField()),
                ('nonCommercial', models.TextField()),
                ('dataLicensing', models.TextField()),
                ('fees', models.TextField()),
                ('limits', models.TextField()),
                ('terms', models.URLField()),
                ('company', models.IntegerField()),
                ('updated', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Mashup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mid', models.URLField()),
                ('title', models.TextField()),
                ('summary', models.TextField()),
                ('rating', models.FloatField()),
                ('name', models.TextField()),
                ('label', models.TextField()),
                ('author', models.TextField()),
                ('description', models.TextField()),
                ('MashupType', models.TextField()),
                ('downloads', models.IntegerField()),
                ('useCount', models.IntegerField()),
                ('sampleUrl', models.URLField()),
                ('dateModified', models.DateTimeField()),
                ('numComments', models.IntegerField()),
                ('commentsUrl', models.URLField()),
                ('Tags', models.TextField()),
                ('APINames', models.TextField()),
                ('APIURLs', models.TextField()),
                ('updated', models.DateTimeField()),
            ],
        ),
    ]
