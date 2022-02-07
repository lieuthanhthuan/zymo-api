# import django
# django.setup()

from django.db import models


class Country(models.Model):
    """Country model records country information
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-name"]
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_name')
        ]


class Region(models.Model):
    """Region model records region information
    """
    name = models.CharField(max_length=255)
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-name"]
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'country'],
                name='unique_country_region_name'
        )]


class CovidStats(models.Model):
    """CovidStats model records covid data for statistic
    """

    confirmed = models.BigIntegerField()
    recovered = models.BigIntegerField()
    deaths = models.BigIntegerField()
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    population = models.BigIntegerField(
        blank=True,
        null=True
    )
    sq_km_area = models.BigIntegerField(
        blank=True,
        null=True
    )
    life_expectancy = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    elevation_in_meters = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )
    continent = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    abbreviation = models.CharField(
        max_length=4,
        blank=True,
        null=True
    )
    location = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    iso = models.IntegerField(
        blank=True,
        null=True
    )
    capital_city = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    lat = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    long = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    updated = models.DateTimeField(
        blank=True,
        null=True
    )

    def __str__(self):
        if not self.region:
            return self.country.name + ' - All'

        return '{0}-{1}'.format(
            self.country.name,
            self.region and self.region.name or '')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['country', 'region'],
                name='unique_country_region'
        )]
