from django.conf import settings
from .geo import get_geo_info
from .geo import get_ip_address
from . import defaults

class GeoAwareSessionMiddleware(object):
    """ Saves geo info in session if GeoIP is configured for city or country.

    geo_info = {
        'fqdn_or_ip': '',
        'city': '', 
        'continent_code': '', 
        'region': '',
        'charset': 0,
        'area_code': 0,
        'longitude': 0.0,
        'country_code3': '',
        'latitude': 0.0,
        'postal_code': None,
        'dma_code': 0,
        'country_code': '',
        'country_name': '',
    }
    """

    def process_request(self, request):
        """ Save or update geo info in session """
        fqdn_or_ip = getattr(defaults, 'GEOIP_DEBUG_DOMAIN_OR_IP', get_ip_address(request))
        try:
            if request.session['geo_info']['fqdn_or_ip'] == fqdn_or_ip:
                return None
        except:
            pass
        geo_info = get_geo_info(request)
        request.session['geo_info'] = geo_info
        request.session.modified = True
        return None
