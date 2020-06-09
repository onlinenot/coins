from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.db.models import Q
from .models import Coin
import requests

URL = settings.API_URL
SKIP = 0
LIMIT = 30

FILTER_BY = (
    ("name", "name"),
    ("-name", "name Reverse"),
    ("-price", "Price"),
    ("price", "Price Reverse"),
)


def homeView(request):
    context = {}
    query = request.GET.get('q', '')
    limit = request.GET.get('limit', LIMIT)
    filter = request.GET.get('filter', "id")
    objects = Coin.objects.filter(
        Q(name__icontains=query)).order_by(filter)
    context["objects"] = objects
    context["query"] = query
    context["filters"] = FILTER_BY
    context["filter"] = filter
    context["api_url"] = URL
    return render(request, 'main/home.html', context)


def api_to_database(request):
    context = {}
    response = {}
    try:
        response = requests.get(f"{URL}?skip={SKIP}&limit={LIMIT}")
    except Exception as err:
        # TODO: Return Http error
        print(f'ERROR: {err}')
        return JsonResponse({"error": "API Faild"}, safe=False)
    else:
        response = response.json()
        for item in response["coins"]:
            Coin.objects.update_or_create(
                name=item["name"],
                coin_id=item["id"],
                symbol=item["symbol"],
                icon=item["icon"],
                defaults={
                    "price": float(item['price']),
                }
            )
    return JsonResponse(response["coins"], safe=False)
