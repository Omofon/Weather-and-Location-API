# Create your views
from django.contrib.gis.utils import GeoIP
from django.template import RequestContext
from django.shortcuts import render_to_response


def home(request):
    g = GeoIP()
    client_ip = request.META["REMOTE_ADDR"]
    lat, long = g.lat_lon(client_ip)
    return render_to_response("home_page_tmp.html", locals())


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
