from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from django.conf import settings
import requests
import urllib

def index(request):
    return HttpResponse("Hello, This is a simple application for serving 1A Api's.")


def get_token(client_id: str, client_secret: str):
    
    
    token_url = settings.ACCESS_TOKEN_URL
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=token_url, client_id=client_id,
        client_secret=client_secret)
    return token

def verify(request: HttpRequest) -> HttpResponse:
    client_id = request.GET.get("client_id", None)
    client_secret = request.GET.get("client_secret", None)

    if client_id is None or client_secret is None:
        return HttpResponseBadRequest("Missing required client_id or client_secret parameters")
    else:
        return prepare_request(client_id, client_secret)

def prepare_request(client_id, client_secret):
    url = settings.FLIGHT_OFFERS_SEARCH_API
    params = {
        "originLocationCode" : "SYD",
        "destinationLocationCode" : "BKK",
        "departureDate" : "2023-10-02",
        "adults" : 2,
        "max" : 5
    }

    token = get_token(client_id, client_secret)['access_token']
    headers = {
        "cache-control": "no-cache",
        "Authorization": f"Bearer {token}"
    }

    api_url = build_url(url, params)
    response = requests.get(api_url, headers=headers)
    if response.json() is not None:
        return HttpResponse(response.json()['data'])
    return HttpResponseBadRequest("The API request did not return any response.")

def build_url( url: str, params: dict ):
    if url == '':
        return HttpResponseBadRequest("The API url is missing in the request.")
    elif params is None:
        return HttpResponseBadRequest("The params are missing in the request.")
    
    split_url = urllib.parse.urlsplit(url)
    split_url = split_url._replace(query=urllib.parse.urlencode(params))

    return urllib.parse.urlunsplit(split_url)