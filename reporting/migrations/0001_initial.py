# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-31 04:54
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='FishCatch',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('weightKgs', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FishingEvent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('RAId', models.CharField(blank=True, max_length=100)),
                ('numberInTrip', models.IntegerField(blank=True)),
                ('targetSpecies', models.CharField(blank=True, max_length=50)),
                ('datetimeAtStart', models.DateTimeField()),
                ('datetimeAtEnd', models.DateTimeField(blank=True)),
                ('committed', models.BooleanField(default=True)),
                ('locationAtStart', django.contrib.postgres.fields.jsonb.JSONField()),
                ('locationAtEnd', django.contrib.postgres.fields.jsonb.JSONField()),
                ('lineString', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
                ('eventSpecificDetails', django.contrib.postgres.fields.jsonb.JSONField()),
                ('mitigationDeviceCodes', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
                ('vesselNumber', models.IntegerField()),
                ('isVesselUsed', models.BooleanField(default=True)),
                ('notes', models.TextField(null=True)),
                ('amendmentReason', models.TextField(null=True)),
                ('archived', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='NonFishingEvent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('seabirdCaptureCode', models.CharField(max_length=3)),
                ('estimatedWeightKg', models.DecimalField(decimal_places=4, max_digits=12)),
                ('numberUninjured', models.IntegerField(null=True)),
                ('numberInjured', models.IntegerField(null=True)),
                ('numberDead', models.IntegerField(null=True)),
                ('tags', django.contrib.postgres.fields.jsonb.JSONField()),
                ('eventHeader', django.contrib.postgres.fields.jsonb.JSONField()),
                ('isVesselUsed', models.BooleanField()),
                ('completed', models.DateTimeField()),
                ('eventVersion', models.DateTimeField()),
                ('notes', models.TextField()),
                ('completedDateTime', models.DateTimeField()),
                ('amendmentReason', models.TextField()),
                ('archived', models.BooleanField()),
                ('fishingEvent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reporting.FishingEvent')),
            ],
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fullName', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Port',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('location', django.contrib.postgres.fields.jsonb.JSONField()),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reporting.Organisation')),
            ],
        ),
        migrations.CreateModel(
            name='ProcessedState',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=3)),
                ('fullName', models.CharField(max_length=50)),
                ('conversionFactor', models.DecimalField(decimal_places=4, max_digits=12)),
            ],
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('speciesType', models.CharField(max_length=20)),
                ('code', models.CharField(max_length=3)),
                ('description', models.CharField(max_length=50, null=True)),
                ('otherNames', models.TextField(max_length=50, null=True)),
                ('fullName', models.CharField(max_length=50, null=True)),
                ('scientificName', models.CharField(max_length=50, null=True)),
                ('image', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('RAId', models.CharField(blank=True, max_length=100)),
                ('personInCharge', models.CharField(max_length=50)),
                ('ETA', models.DateTimeField()),
                ('startTime', models.DateTimeField()),
                ('endTime', models.DateTimeField()),
                ('startLocation', django.contrib.postgres.fields.jsonb.JSONField()),
                ('endLocation', django.contrib.postgres.fields.jsonb.JSONField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reporting.Organisation')),
                ('unloadPort', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reporting.Port')),
            ],
        ),
        migrations.CreateModel(
            name='Vessel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('registration', models.IntegerField()),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reporting.Organisation')),
            ],
        ),
        migrations.AddField(
            model_name='trip',
            name='vessel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reporting.Vessel'),
        ),
        migrations.AddField(
            model_name='processedstate',
            name='species',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reporting.Species'),
        ),
        migrations.AddField(
            model_name='nonfishingevent',
            name='nonFishProtectedSpecies',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reporting.Species'),
        ),
        migrations.AddField(
            model_name='nonfishingevent',
            name='trip',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reporting.Trip'),
        ),
        migrations.AddField(
            model_name='fishingevent',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reporting.Trip'),
        ),
        migrations.AddField(
            model_name='fishcatch',
            name='fishingEvent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fishCatches', to='reporting.FishingEvent'),
        ),
        migrations.AddField(
            model_name='fishcatch',
            name='species',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reporting.Species'),
        ),
        migrations.AddField(
            model_name='user',
            name='organisation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reporting.Organisation'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
