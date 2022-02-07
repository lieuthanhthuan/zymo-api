
import json
from datetime import datetime
from zymo_api.models import Country, Region, CovidStats

f = open('data/covid-stats.json')
data = json.load(f)
 

def get_country(country_name):
    try:
        return Country.objects.get(
            name=country_name)
    except Country.DoesNotExist:
        return None

def get_region(country_id, region_name):
    try:
        return Region.objects.get(
            country__id=country_id,
            name=region_name)
    except Region.DoesNotExist:
        return None

# Iterating through the json
# list
for country_name, data in data.items():
    country = get_country(country_name)

    if not country:
        country = Country.objects.create(name=country_name)

    for region_name, covidstas in data.items():
        region_id = None
        region = None
        if region_name != 'All':
            region = get_region(
                country_id=country.id,
                region_name=region_name
            )

            if not region:
                region = Region.objects.create(
                    country=country,
                    name=region_name)
            region_id = region.id

        existing_rec = None
        try:
            existing_rec = CovidStats.objects.filter(
            country__id=country.id,
            region__id=region_id
        )
        except CovidStats.DoesNotExist:
            pass

        if 'updated' in covidstas:
            updated = datetime.strptime(
                covidstas['updated'][:18], '%Y/%m/%d %H:%M:%S')
            updated.strftime('YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]')
            covidstas['updated'] = updated

        covidstas['country'] = country
        if not existing_rec:
            CovidStats.objects.create(region=region, **covidstas)

# Closing file
f.close()
