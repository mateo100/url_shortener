import json
import string
import random
import validators
from urllib.parse import urlparse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.decorators import api_view
from .env import SHORT_URL_LENGTH
from .models import URL


def generate_random_string():
    """Generates a random string which is short version of url"""
    characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(SHORT_URL_LENGTH))


@api_view(['POST'])
def generate_short_url(request):
    """Generate short url for provided long url"""
    try:
        params = json.loads(request.body.decode('utf-8'))
        long_url = params['url']
    except (ValueError, KeyError):
        response = {'status': 'error', 'message': 'Some error occurs'}
        return HttpResponse(json.dumps(response), 'application/json', status=400)

    if not validators.url(long_url):
        response = {'status': 'error', 'message': 'Invalid URL'}
        return HttpResponse(json.dumps(response), 'application/json', status=400)

    scheme = urlparse(long_url).scheme
    cut_long_url = long_url.replace('www.', '').replace(scheme + '://', '')

    try:
        url_obj = URL.objects.get(Q(scheme=scheme), Q(long_url=cut_long_url) | Q(long_url__endswith=cut_long_url))
        short_url = url_obj.short_url
    except URL.DoesNotExist:
        short_url = generate_random_string()
        url_obj = URL(long_url=cut_long_url, short_url=short_url, scheme=scheme)
        url_obj.save()

    response = {'status': "success", 'short_url': short_url}
    return HttpResponse(json.dumps(response), content_type='application/json', status=200)


@api_view(['GET'])
def redirect_to_appropriate_url(request, short_url):
    """Redirect to appropriate page using domain and short url"""
    try:
        url_obj = URL.objects.get(short_url=short_url)
        return HttpResponseRedirect(url_obj.scheme + '://' + url_obj.long_url)
    except URL.DoesNotExist:
        response = {'status': 'error', 'message': 'No url was recognized.'}
        return HttpResponse(json.dumps(response), 'application/json', status=400)
