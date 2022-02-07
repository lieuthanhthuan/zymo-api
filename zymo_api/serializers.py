from django.contrib.auth.models import User
from rest_framework import serializers
from .models import CovidStats


class CountrySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)


class RegionSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)


class CovidStatsSerializer(serializers.ModelSerializer):
    country_id = serializers.PrimaryKeyRelatedField(
        many=False, read_only=True)
    region_id = serializers.PrimaryKeyRelatedField(
        many=False, read_only=True)
    country = serializers.CharField()
    region = serializers.CharField()

    class Meta:
        model = CovidStats
        fields = "__all__"

    def to_representation(self, instance):
        representation = super(
            CovidStatsSerializer,
            self
        ).to_representation(instance)
        representation['country'] = instance.country.name
        representation['region'] = \
            instance.region and instance.region.name or 'All'

        return representation


class CovidStatsCountrySerializer(serializers.ModelSerializer):
    country_id = serializers.PrimaryKeyRelatedField(
        many=False, read_only=True)
    region_id = serializers.PrimaryKeyRelatedField(
        many=False, read_only=True)
    country = serializers.CharField(read_only=True)
    region = serializers.CharField(read_only=True)

    class Meta:
        model = CovidStats
        fields = "__all__"

    def to_representation(self, instance):
        representation = super(CovidStatsCountrySerializer, self).to_representation(instance)
        representation['country'] = instance.country.name
        representation['region'] = instance.region and instance.region.name or 'All'
        return representation
