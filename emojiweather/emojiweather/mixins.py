from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import requests


class CsrfExemptMixin:
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class WeatherFormMixin:
    def get_geocode(self, address):
        key = settings.GOOGLE_GEOCODING_API_KEY
        url = 'https://maps.googleapis.com/maps/api/geocode/json'
        r = requests.get(url, params={'address': address, 'key': key})
        j = r.json()
        if j['status'] == 'OK':
            return j['results'][0]
        else:
            errors = {
                'zero_results': 'We\u2019re sorry, but we could not find %s.' % address,
                'over_query_limit': 'We\u2019re sorry, but the request quota has been reached.',
                'request_denied': 'We\u2019re sorry, but the request was denied.',
                'invalid_request': 'We\u2019re sorry, but the request was invalid.',
                'unknown': 'We\u2019re sorry, but an error occurred.',
            }
            try:
                return errors[j['status'].lower()]
            except KeyError:
                return errors['unknown']

    def get_weather(self, geocode):
        key = settings.DARK_SKY_API_KEY
        latitude = geocode['geometry']['location']['lat']
        longitude = geocode['geometry']['location']['lng']
        units = 'auto'
        url = 'https://api.darksky.net/forecast/%s/%s,%s' % (key, latitude, longitude)
        r = requests.get(url, params={'units': units})
        return r.json()

    def get_temperature(self, weather):
        temp = weather['currently']['temperature']
        units = weather['flags']['units']
        data = {}
        if units == 'us':
            data['f'] = temp
            data['c'] = (temp - 32) * 5 / 9
        else:
            data['f'] = (temp * 9 / 5) + 32
            data['c'] = temp
        return data

    def get_results(self, address):
        results = {}
        geocode = self.get_geocode(address)
        if isinstance(geocode, str):
            results['error'] = geocode
        else:
            results['geocode'] = geocode
            results['weather'] = self.get_weather(geocode)
            results['temperature'] = self.get_temperature(results['weather'])
        return results
