from django.http import Http404
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from zymo_api.models import CovidStats, Country, Region
from .serializers import CovidStatsSerializer, CovidStatsCountrySerializer


def get_country(country_id=None, country_name=None):
    """
    Get country by name or by country id

        Parameters:
            country_id (int): country id
            country_name (str): Country name

        Returns:
            Country (Country): a country object
    """
    try:
        if country_id:
            return Country.objects.get(
                pk=country_id)
        else:
            country = Country.objects.filter(
                name=country_name
            )
            if country:
                return Country.objects.get(
                name=country_name)
            if country_name:
                return Country.objects.create(name=country_name)
    except CovidStats.DoesNotExist:
        raise Http404

def get_region(region_name, country_id):
    """
    Get region by name

        Parameters:
            region_name (str): Country name

        Returns:
            Country (Country): a country object
    """
    try:
        if Region.objects.filter(name=region_name,country__id=country_id):
            return Region.objects.get(
            name=region_name,
            country__id=country_id
        )
        else:
            return Region.objects.create(
                name=region_name,
                country_id=country_id
            )
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
        country = get_country(country_name=country_name)
        data['country'] = country

        # remove region from data
        region = None
        region_name = data.pop('region', None)
        region_id = None
        if region_name:
            # find the region object
            region = get_region(region_name, country.id)
        data['region'] = region

        existing_rec = CovidStats.objects.filter(
            country__id=country.id,
            region__id=region_id
        )

        if not existing_rec:
            new_covid_stats = CovidStats.objects.create(**data)
            new_covid_stats.save()
            return new_covid_stats
        else:
            return None

    def create(self, request, *args,**kwargs):
        data = request.data
        many = isinstance(data, list)

        if not many:
            new_covidstas = self.create_covidstas(data)
        else:
            for item in data:
                new_covidstas = self.create_covidstas(item)

        if not new_covidstas:
            return Response(
                data={'message': 'Covid Stats already exist!'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CovidStatsSerializer(new_covidstas)
        return Response(serializer.data)



class CovidStatsCountry(
    generics.CreateAPIView,
    generics.RetrieveUpdateDestroyAPIView
    ):
    """
        Api to get, create, post, put, delete data for specific country
    """

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
        region_id = None
        region_name = data.pop('region', None)

        if region_name:
            # find the region object
            region = get_region(region_name, country_id)
            region_id = region.id

        data['region'] = region

        # checking uniqe country region constraint
        existing_rec = CovidStats.objects.filter(
            country__id=country_id,
            region__id=region_id
        )

        if not existing_rec:
            new_covid_stats = CovidStats.objects.create(**data)
            new_covid_stats.save()
            serializer = CovidStatsCountrySerializer(new_covid_stats)
            return Response(serializer.data)
        else:
            return Response(
                data={'message': 'Covid Stats already exist!'},
                status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):

        data = request.data
        country_id = self.kwargs['countryId']

        # remove region from data
        region = None
        region_name = data.get('region', None)
        if region_name:
            # find the region object
            region = get_region(region_name)
            data['region'] = region

        else:
            data['region'] = None
        exist_record = None
        if region:
            exist_record = CovidStats.objects.filter(
                country__id=country_id,
                region__id=region.id
            )

        else:
            exist_record = CovidStats.objects.filter(
                country__id=country_id,
                region__id__isnull=True
            )

        if exist_record:
            exist_record.update(**data)
            updated_record = self.get_object()

            serializer = CovidStatsCountrySerializer(updated_record)
            return Response(serializer.data)

        else:
            Response(
                data={'message': 'Covid Stats does not exist!'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, *args, **kwargs):
        # find the Country object
        covidstats = self.get_object()
        covidstats.delete()
        return Response(data={'message': 'Covid Stats is deleted successfully!'}, status=status.HTTP_200_OK)


class CovidStatsCountryRegions(
    generics.ListAPIView):
    """
        Api to get all regional data within an existing country
    """
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
        serializer = covidstats
        return covidstats


class CovidStatsCountryRegion(
    generics.ListAPIView,
    generics.UpdateAPIView):
    """
        Api to get, create, post, put, delete a specific region
        within an existing country
    """

    queryset = CovidStats.objects.all()
    model = CovidStats
    serializer_class = CovidStatsCountrySerializer

    def get_object(self):
        """
        This view should return a list of all the CovidStats for
        the CovidStats as determined by the countryId and regionId
        portion of the URL.
        """

        country_id = self.kwargs['countryId']
        region_id = self.kwargs['regionId']
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

    def update(self, request, *args, **kwargs):
        data = request.data
        exist_record = self.get_object()

        if exist_record:
            exist_record.update(**data)

            updated = CovidStats.objects.get(
                    country__id=self.kwargs['countryId'],
                    region__id=self.kwargs['regionId']
                )
            serializer = CovidStatsCountrySerializer(updated)
            return Response(serializer.data)

        else:
            return Response(
                data={'message': 'Covid Stats does not exist!'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, *args, **kwargs):
        covidstats = self.get_object()

        if not covidstats:
            return Response(
                data={'message': 'CovidStats does not exist!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        covidstats.delete()
        return Response(
            data={'message': 'CovidStats is deleted successfully!'},
            status=status.HTTP_200_OK
        )
