import urllib.request
import json
from django.http import JsonResponse
from ipware import get_client_ip as ipware_get_client_ip
from geoip2.database import Reader
import os
from django.conf import settings


def get_visitor_name(request):
    visitor_name = request.GET.get("visitor_name", "Guest")
    if visitor_name.startswith('"') and visitor_name.endswith('"'):
        visitor_name = visitor_name[1:-1]
    return visitor_name


def get_client_ip(request):
    client_ip, is_routable = ipware_get_client_ip(request)
    if client_ip is None or client_ip == "127.0.0.1":
        client_ip = "8.8.8.8"
    return client_ip


def get_city(client_ip):
    reader = Reader(os.path.join(settings.GEOIP_PATH, "GeoLite2-City.mmdb"))
    try:
        client_ip = str(client_ip)
        response = reader.city(client_ip)
        city = response.city.name
        if not city:
            return "Lagos"
        return city
    except Exception as e:
        print(f"GeoIP lookup error: {e}. Using default city: Lagos.")
        return "Lagos"


def get_temperature(city):
    api_key = "edadf75d586f1b7214898ad91e2d6077"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

    try:
        response = urllib.request.urlopen(url)
        source = response.read()

        list_of_data = json.loads(source)
        temp_kelvin = list_of_data["main"]["temp"]
        temp_celsius = temp_kelvin - 273.15

        return round(temp_celsius, 2)
    except Exception as e:
        print(f"Error fetching temperature data: {e}")
        return "Unknown temp"


def print_json(data):
    return JsonResponse(data)


def hello(request):
    if request.method == "GET":
        try:
            visitor_name = get_visitor_name(request)
            client_ip = get_client_ip(request)
            city = get_city(client_ip)
            temperature = get_temperature(city)
            greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celcius in {city}"

            response_data = {
                "client_ip": client_ip,
                "location": city,
                "greeting": greeting,
            }
            return print_json(response_data)

        except Exception as e:
            print(f"Error in hello view: {e}")
            return JsonResponse(
                {"error": "An error occurred while processing your request."},
                status=500,
            )
