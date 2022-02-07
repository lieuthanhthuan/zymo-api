from rest_framework.test import APITestCase
from zymo_api.models import Country


class TestApi(APITestCase):
    def test_get_countries(self):
        response = self.client.get('http://localhost:3001/countries/')
        assert response.status_code == 200

    def test_search_countries(self):
        response = self.client.get('http://localhost:3001/countries/search/Al/')
        assert response.status_code == 200

    def test_get_country(self):
        response = self.client.get('http://localhost:3001/country/1/')
        assert response.status_code == 404

    def test_get_country_region(self):
        response = self.client.get('http://localhost:3001/country/1/region/1/')
        assert response.status_code == 200

    def test_get_country_regions(self):
        response = self.client.get('http://localhost:3001/country/1/regions/')
        assert response.status_code == 200

    def test_post_country(self):
        Country.objects.create(name="Afghanistan")
        data = {
            "country": "Afghanistan",
            "region": "",
            "confirmed": 1575421,
            "recovered": 0,
            "deaths": 7317,
            "population": 35530081,
            "sq_km_area": 652090,
            "life_expectancy": "45.9",
            "elevation_in_meters": 0,
            "continent": "Asia",
            "abbreviation": "AF",
            "location": "Southern and Central Asia",
            "iso": 4,
            "capital_city": "Kabul",
            "lat": "33.93911",
            "long": "67.709953",
            "updated": "2021-12-09T01:23:00Z"
        }
        response = self.client.post('/country/', data)
        assert response.status_code == 200
        assert response.data.get('country') == "Afghanistan"
        assert response.data.get('region') == "All"

    def test_post_country_id(self):
        country = Country.objects.create(name="Albania")
        data = {
            "region": "",
            "confirmed": 1575421,
            "recovered": 0,
            "deaths": 7317,
            "population": 35530081,
            "sq_km_area": 652090,
            "life_expectancy": "45.9",
            "elevation_in_meters": 0,
            "continent": "Asia",
            "abbreviation": "AF",
            "location": "Southern and Central Asia",
            "iso": 4,
            "capital_city": "Kabul",
            "lat": "33.93911",
            "long": "67.709953",
            "updated": "2021-12-09T01:23:00Z"
        }
        url = '/country/{0}/'.format(str(country.id))
        response = self.client.post(url, data)
        assert response.status_code == 200
        assert response.data.get('country') == "Albania"
        assert response.data.get('region') == "All"

    def test_put_country(self):
        country = Country.objects.create(name="Algeria")
        data = {
            "region": "",
            "confirmed": 1575421,
            "recovered": 0,
            "deaths": 7317,
            "population": 35530081,
            "sq_km_area": 652090,
            "life_expectancy": "45.9",
            "elevation_in_meters": 0,
            "continent": "Asia",
            "abbreviation": "AF",
            "location": "Southern and Central Asia",
            "iso": 4,
            "capital_city": "Kabul",
            "lat": "33.93911",
            "long": "67.709953",
            "updated": "2021-12-09T01:23:00Z"
        }
        url = '/country/{0}/'.format(str(country.id))
        response = self.client.post(url, data)
        assert response.status_code == 200
        assert response.data.get('country') == "Algeria"
        assert response.data.get('region') == "All"

        update_data = {
            "region": "",
            "confirmed": 1575423,
            "recovered": 0,
            "deaths": 8012,
            "population": 355300811,
            "sq_km_area": 652090,
            "life_expectancy": "45.9",
            "elevation_in_meters": 0,
            "continent": "Asia",
            "abbreviation": "AF",
            "location": "Southern and Central Asia",
            "iso": 4,
            "capital_city": "Kabul",
            "lat": "33.93911",
            "long": "67.709953",
            "updated": "2021-12-09T01:23:00Z"
        }
        update_response = self.client.put(url, update_data)
        assert update_response.status_code == 200
        assert update_response.data.get('country') == "Algeria"
        assert update_response.data.get('region') == "All"
        assert update_response.data.get('confirmed') == 1575423
        assert update_response.data.get('recovered') == 0
        assert update_response.data.get('deaths') == 8012
        assert update_response.data.get('population') == 355300811
        assert update_response.data.get('sq_km_area') == 652090

    def test_delete_country(self):
        country = Country.objects.create(name="Andorra")
        data = {
            "region": "",
            "confirmed": 1575421,
            "recovered": 0,
            "deaths": 7317,
            "population": 35530081,
            "sq_km_area": 652090,
            "life_expectancy": "45.9",
            "elevation_in_meters": 0,
            "continent": "Asia",
            "abbreviation": "AF",
            "location": "Southern and Central Asia",
            "iso": 4,
            "capital_city": "Kabul",
            "lat": "33.93911",
            "long": "67.709953",
            "updated": "2021-12-09T01:23:00Z"
        }
        url = '/country/{0}/'.format(str(country.id))
        response = self.client.post(url, data)
        assert response.status_code == 200
        assert response.data.get('country') == "Andorra"
        assert response.data.get('region') == "All"

        del_response = self.client.delete(url)
        assert del_response.status_code == 200
