from django.http import Http404
from rest_framework import status
from rest_framework import generics, views
from rest_framework.response import Response
from zymo_api.models import CovidStats, Country, Region
from .serializers import CovidStatsSerializer, CovidStatsCountrySerializer

def get_country(country_id):
    try:
        return Country.objects.get(
            pk=country_id)
    except CovidStats.DoesNotExist:
        raise Http404

def get_region(region_name):
    try:
        return Region.objects.get(
            name=region_name)
    except CovidStats.DoesNotExist:
        raise Http404

class CovidStatsList(generics.ListAPIView):
    """Gets all data for all countries
    """
    queryset = CovidStats.objects.all()
    serializer_class = CovidStatsSerializer

    def get_queryset(self):
        """
        This view should return a list of all the CovidStatsList for
        the CovidStatsList as determined by the country name portion of the URL.
        """
        country = self.kwargs.get('country', False)
        if not country:
            return CovidStats.objects.all()
        else:
            return CovidStats.objects.filter(
                country__name__contains=country)


class CovidStatsPost(generics.CreateAPIView):
    """View to post a country object, can include regional data
    """
    queryset = CovidStats.objects.all()
    serializer = CovidStatsSerializer(queryset, many=True)
    serializer_class = CovidStatsSerializer

    def create_covidstas(self, data):
        """Create a new CovidStats record
        """

        # remove country from the data
        country_name = data.pop('country', None)
        # find the Country object
        country = Country.objects.get(name=country_name)
        data['country'] = country

        # remove region from data
        region = None
        region_name = data.pop('region', None)
        if region_name:
            # find the region object
            region = Region.objects.get(name=region_name)
        data['region'] = region

        new_covid_stats = CovidStats.objects.create(**data)
        new_covid_stats.save()

        return new_covid_stats

    def create(self, request, *args,**kwargs):
        data = request.data
        many = isinstance(data, list)

        if not many:
            new_covidstas = self.create_covidstas(data)
        else:
            for item in data:
                new_covidstas = self.create_covidstas(item)

        serializer = CovidStatsSerializer(new_covidstas)
        return Response(serializer.data)


class CovidStatsCountry(
    generics.CreateAPIView,
    generics.RetrieveUpdateDestroyAPIView
    ):

    queryset = CovidStats.objects.all()
    model = CovidStats
    serializer_class = CovidStatsCountrySerializer
    lookup_field = 'country'

    def get_object(self):
        """Get CovidStats by countryId
        """
        country_id = self.kwargs['countryId']
        try:
            return CovidStats.objects.get(
                country__id=country_id,
                region__id__isnull=True)
        except CovidStats.DoesNotExist:
            raise Http404

    def get_queryset(self):
        """
        This view should return a list of all the CovidStatsList for
        the CovidStatsList as determined by the country name portion of the URL.
        """

        covidstats = self.get_object()
        serializer = CovidStatsCountrySerializer(covidstats)
        return Response(serializer.data)

    def create(self, request, *args,**kwargs):
        data = request.data

        # remove country from the comment data
        country_id = self.kwargs['countryId']
        # find the Country object
        country = get_country(country_id)
        data['country'] = country

        # remove region from the comment data
        region = None
        region_name = data.pop('region', None)

        if region_name:
            # find the region object
            region = get_region(region_name)

        data['region'] = region

        new_covid_stats = CovidStats.objects.create(**data)
        new_covid_stats.save()

        serializer = CovidStatsSerializer(new_covid_stats)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):

        data = request.data
        country_id = self.kwargs['countryId']

        # remove region from data
        region = None
        region_name = data.pop('region', None)
        if region_name:
            # find the region object
            region = Region.objects.get(name=region_name)
        if region:
            exist_record = CovidStats.objects.filter(
                country__id=country_id,
                region__id=region.id
            )[:1]
        else:
            exist_record = CovidStats.objects.filter(
                country__id=country_id,
                region__id__isnull=True
            )[:1]

        exist_record.update(**data)
        serializer = CovidStatsCountrySerializer(exist_record)

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        # find the Country object
        covidstats = self.get_object()
        covidstats.delete()
        return Response(status=status.HTTP_200_OK)


class CovidStatsCountryRegions(
    generics.ListAPIView):
    queryset = CovidStats.objects.all()
    model = CovidStats
    serializer_class = CovidStatsSerializer

    def get_object(self):
        country_id = self.kwargs['countryId']
        try:
            return CovidStats.objects.filter(
                    country__id=country_id
                )
        except CovidStats.DoesNotExist:
            raise Http404

    def get_queryset(self):
        """
        This view should return a list of all the CovidStatsList for
        the CovidStatsList as determined by the country name portion of the URL.
        """

        covidstats = self.get_object()
        return covidstats


class CovidStatsCountryRegion(
    generics.ListAPIView):
    queryset = CovidStats.objects.all()
    model = CovidStats
    serializer_class = CovidStatsSerializer

    def get_object(self):
        """
        This view should return a list of all the CovidStats for
        the CovidStats as determined by the countryId and regionId
        portion of the URL.
        """

        country_id = self.kwargs['countryId']
        region_id = self.kwargs.get('regionId', False)
        try:
            if not region_id:
                return CovidStats.objects.filter(
                    country__id=country_id,
                    region__id__isnull=True
                )
            return CovidStats.objects.filter(
                    country__id=country_id,
                    region__id=region_id
                )
        except CovidStats.DoesNotExist:
            raise Http404

    def get_queryset(self):
        covidstats = self.get_object()
        return covidstats

    def delete(self, request, *args, **kwargs):
        covidstats = self.get_object()
        covidstats.delete()
        return Response(status=status.HTTP_200_OK)
